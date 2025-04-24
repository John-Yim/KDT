# app/routes/main.py
import os
import pandas as pd
from flask import Blueprint, render_template, redirect, url_for, current_app, request, jsonify
from app.models.project_model import get_all_projects, get_project_by_id

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
def index():
    projects = get_all_projects()
    return render_template("index.html", projects=projects)

@main_bp.route("/view_demo/<int:project_id>/")
def view_demo(project_id):
    project = get_project_by_id(project_id)

    if not project:
        return redirect(url_for("main_bp.index"))
    
    if project_id == 1:
        return redirect(url_for("brain_bp.brain_demo"))
    elif project_id == 2:
        return redirect(url_for("complaint_bp.complaint_demo"))
    else:
        return redirect(url_for("main_bp.index"))

@main_bp.route("/view_html/<int:project_id>/")
def view_html(project_id):
    project = get_project_by_id(project_id)
    if not project:
        return render_template("error.html", message="프로젝트 정보를 찾을 수 없습니다.")
    
    html_path = project.get("project_html_path")
    if not html_path:
        return render_template("error.html", message="코드 HTML 파일이 없습니다.")
    
    file_path = os.path.join(current_app.root_path, "static", html_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception as e:
        return render_template("error.html", message="파일을 읽을 수 없습니다: " + str(e))
    
    return render_template("view.html", code=file_content)

# 데이터 분석(data_analysis) 페이지 ----------------------
@main_bp.route('/data_analysis/', methods=['GET'])
def data_analysis():
    path1 = os.path.join(current_app.root_path, 'static', 'html', '1_데이터셋구조.html')
    try:
        with open(path1, 'r', encoding='utf-8') as f:
            content1 = f.read()
    except Exception as e:
        content1 = f"<p>1_데이터셋구조.html 로드 실패: {e}</p>"

    path2 = os.path.join(current_app.root_path, 'static', 'html', '2_데이터전처리.html')
    try:
        with open(path2, 'r', encoding='utf-8') as f:
            content2 = f.read()
    except Exception as e:
        content2 = f"<p>2_데이터전처리.html 로드 실패: {e}</p>"

    path3 = os.path.join(current_app.root_path, 'static', 'html', '3_상관관계분석.html')
    try:
        with open(path3, 'r', encoding='utf-8') as f:
            content3 = f.read()
    except Exception as e:
        content3 = f"<p>3_상관관계분석.html 로드 실패: {e}</p>"

    return render_template('data_analysis.html', content=content1, content2=content2, content3=content3)