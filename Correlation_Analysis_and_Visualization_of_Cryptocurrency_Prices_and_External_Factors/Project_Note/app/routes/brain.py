# app/routes/brain.py
from flask import Blueprint, render_template, request, current_app
import numpy as np
import tensorflow as tf
import cv2
import base64
import os
from app.models.project_model import get_project_by_id

brain_bp = Blueprint('brain_bp', __name__)

def preprocess_image(file_bytes, target_size=224):
    npimg = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if image is None:
        return None
    h, w = image.shape[:2]
    scale_ratio = target_size / max(h, w)
    new_w, new_h = int(w * scale_ratio), int(h * scale_ratio)
    resized_image = cv2.resize(image, (new_w, new_h))
    padded_image = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    y_offset = (target_size - new_h) // 2
    x_offset = (target_size - new_w) // 2
    padded_image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_image
    return np.expand_dims(padded_image / 255.0, axis=0)

@brain_bp.route("/", methods=['GET', 'POST'])
def brain_demo():
    project = get_project_by_id(1)

    prediction = None
    uploaded_image = None

    if not project:
        return render_template("error.html", message="프로젝트 정보를 찾을 수 없습니다.")
    
    model_dir = os.path.join(current_app.root_path, project["project_model_path"])
    model_path = os.path.join(model_dir, 'Fine.h5')
    brain_model = tf.keras.models.load_model(model_path)

    idx_to_class = {0: 'notumor', 1: 'glioma', 2: 'meningioma', 3: 'pituitary'}

    if request.method == 'POST':
        base64_image = request.form.get('image_base64')
        if base64_image:
            header, encoded = base64_image.split(',', 1)
            file_bytes = base64.b64decode(encoded)
            uploaded_image = base64_image
            input_img = preprocess_image(file_bytes)
            if input_img is not None:
                pred = brain_model.predict(input_img)[0]
                label_idx = np.argmax(pred)
                prediction = f"{idx_to_class[label_idx]} ({pred[label_idx]*100:.2f}%)"

    return render_template("demo_view_brain.html", prediction=prediction, uploaded_image=uploaded_image, project={"project_image_path": project["project_image_path"]})