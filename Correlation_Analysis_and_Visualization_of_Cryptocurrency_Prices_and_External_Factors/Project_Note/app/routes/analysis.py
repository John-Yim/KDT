from flask import Blueprint, request, jsonify, current_app
import os
import pandas as pd

analysis_bp = Blueprint("analysis", __name__)

# ------------------------ AJAX용 데이터셋 구조 시각화 API ------------------------
@analysis_bp.route('/dataset_structure', methods=['GET'])
def dataset_structure():
    dataset_name = request.args.get('dataset')
    allowed_files = [
        '비트코인_23.01.01~25.01.31.csv',
        '이더리움_23.01.01~25.01.31.csv',
        '도지코인_23.01.01~25.01.31.csv',
        '코스피_23.01.01~25.01.31.csv',
        '나스닥_23.01.01~25.01.31.csv',
        '한국금리_23.01.01~25.01.31.csv',
        '미국금리_23.01.01~25.01.31.csv',
        '월령_23.01.01~25.01.31.csv',
        '날씨_23.01.01~25.01.31.csv'
    ]
    if dataset_name not in allowed_files:
        return jsonify({"error": "유효하지 않은 데이터셋 파일입니다."}), 400

    path = os.path.join(current_app.root_path, 'static', 'dataset', dataset_name)
    if not os.path.exists(path):
        return jsonify({"error": f"파일이 존재하지 않습니다: {path}"}), 500

    try:
        try:
            df = pd.read_csv(path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(path, encoding='EUC-KR')
    except Exception as e:
        return jsonify({"error": "데이터셋 로드에 실패했습니다: " + str(e)}), 500

    return jsonify({
        "head": df.head(3).to_html(classes="table table-bordered"),
        "dtypes": df.dtypes.to_frame("dtype").to_html(classes="table table-bordered"),
        "isna": df.isna().sum().to_frame("na_count").to_html(classes="table table-bordered"),
        "nunique": df.nunique().to_frame("unique count").to_html(classes="table table-bordered"),
        "describe": df.describe().to_html(classes="table table-bordered")
    })


# ------------------------ AJAX용 데이터셋 차트 시각화 API ------------------------
@analysis_bp.route('/dataset_viz', methods=['GET'])
def dataset_viz():
    dataset_name = request.args.get('dataset')
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    allowed_files = [
        '비트코인_23.01.01~25.01.31.csv',
        '이더리움_23.01.01~25.01.31.csv',
        '도지코인_23.01.01~25.01.31.csv',
        '코스피_23.01.01~25.01.31.csv',
        '나스닥_23.01.01~25.01.31.csv',
        '한국금리_23.01.01~25.01.31.csv',
        '미국금리_23.01.01~25.01.31.csv',
        '월령_23.01.01~25.01.31.csv',
        '날씨_23.01.01~25.01.31.csv'
    ]
    if dataset_name not in allowed_files:
        return jsonify({"error": "유효하지 않은 데이터셋 파일입니다."}), 400

    path = os.path.join(current_app.root_path, 'static', 'dataset', dataset_name)
    if not dataset_name or not os.path.exists(path):
        return jsonify({"error": f"Invalid dataset: {dataset_name}"}), 500

    try:
        try:
            df = pd.read_csv(path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(path, encoding='EUC-KR')
    except Exception as e:
        return jsonify({"error": "데이터셋 로드 실패: " + str(e)}), 500

    try:
        columns = df.columns.tolist()
        counts = df.count().tolist()
        missing = df.isna().sum().tolist()

        return jsonify({
            "columns": columns,
            "counts": counts,
            "missing": missing
        })
    except Exception as e:
        return jsonify({"error": "데이터셋 시각화 로드 실패: " + str(e)}), 500


# ------------------------ AJAX용 전처리 데이터셋 시각화 API ------------------------
@analysis_bp.route('/preproc_viz', methods=['GET'])
def preproc_viz():
    viz_type = request.args.get("type")  # 'raw' 또는 'norm'
    cols = request.args.get("cols", "")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    if viz_type not in ['raw', 'norm']:
        return jsonify({"error": "유효하지 않은 type 파라미터입니다. (raw 또는 norm)"}), 400

    file_name = "암호화폐_금리_지수_월령_날씨_병합데이터.csv" if viz_type == 'raw' else "암호화폐_금리_지수_월령_날씨_병합데이터_정규화.csv"
    file_path = os.path.join(current_app.root_path, "static", "dataset", file_name)
    if not os.path.exists(file_path):
        return jsonify({"error": f"파일이 존재하지 않습니다: {file_path}"}), 500

    selected_cols = [c.strip() for c in cols.split(",") if c.strip().lower() != 'date'] if cols else []

    try:
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='EUC-KR')
    except Exception as e:
        return jsonify({"error": "데이터셋 로드 실패: " + str(e)}), 500

    if 'date' not in df.columns:
        return jsonify({"error": "'date' 컬럼이 없습니다."}), 500
    try:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    except Exception as e:
        return jsonify({"error": "날짜 변환 실패: " + str(e)}), 500

    if from_date and to_date:
        try:
            f_date = pd.to_datetime(from_date)
            t_date = pd.to_datetime(to_date)
            df = df[(df['date'] >= f_date) & (df['date'] <= t_date)]
        except Exception as e:
            return jsonify({"error": "날짜 필터링 실패: " + str(e)}), 500

    dates = df['date'].dt.strftime('%Y-%m-%d').tolist()
    data_dict = {col: df[col].tolist() for col in selected_cols if col in df.columns}
    weather_cols = ['partly_cloudy', 'snow', 'clear', 'rain', 'cloudy']
    weather_dict = {col: df[col].tolist() for col in weather_cols if col in df.columns}

    return jsonify({
        "dates": dates,
        "data": data_dict,
        "weather": weather_dict
    })
