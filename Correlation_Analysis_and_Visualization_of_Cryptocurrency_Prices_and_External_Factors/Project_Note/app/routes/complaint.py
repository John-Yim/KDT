# app/routes/complaint.py
from flask import Blueprint, render_template, request, current_app
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pickle
import os
from app.db import get_db
from app.models.project_model import get_project_by_id

complaint_bp = Blueprint('complaint_bp', __name__)

def get_gov_info(category):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gov_infos WHERE gov_category = %s LIMIT 1", (category,))
    return cursor.fetchone()

@complaint_bp.route("/", methods=["GET", "POST"])
def complaint_demo():
    project = get_project_by_id(2)

    result = None
    gov_info = None

    if not project:
        return render_template("error.html", message="프로젝트 정보를 찾을 수 없습니다.")
    
    model_path = os.path.join(current_app.root_path, project["project_model_path"])

    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    with open(os.path.join(model_path, 'label_encoder.pkl'), 'rb') as f:
        label_encoder = pickle.load(f)
    
    if request.method == 'POST':
        text = request.form.get('complaint')
        if text:
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding='max_length', max_length=256)
            if 'token_type_ids' in inputs:
                inputs['token_type_ids'] = torch.zeros_like(inputs['input_ids'])
            
            with torch.no_grad():
                outputs = model(**inputs)
                pred_id = torch.argmax(outputs.logits, dim=1).item()
                category = label_encoder.inverse_transform([pred_id])[0]
                result = {"category": category}
                gov_info = get_gov_info(category)

    return render_template("demo_view_complaint.html", result=result, gov_info=gov_info, project={"project_image_path": project["project_image_path"]})