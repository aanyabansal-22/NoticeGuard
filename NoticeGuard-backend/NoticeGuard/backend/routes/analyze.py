from flask import Blueprint, request, jsonify
from services.rule_engine import analyze_rules
from services.ocr_service import extract_text_from_file
from services.ai_service import analyze_with_ai
from utils.text_utils import clean_text

analyze_bp = Blueprint("analyze", __name__)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze_notice():
    try:
        text = request.form.get("text", "").strip()
        uploaded_file = request.files.get("file")

        if not text and not uploaded_file:
            return jsonify({
                "error": (
                    "Please provide notice text "
                    "or upload a PDF/image."
                )
            }), 400

        if uploaded_file and not text:
            extracted_text = extract_text_from_file(uploaded_file)
            text = extracted_text

        text = clean_text(text)
        if not text:
            return jsonify({
                "error": "Unable to extract readable text."
            }), 400

        rule_result = analyze_rules(text)
        ai_result = analyze_with_ai(text, rule_result)
        final_result = build_final_result(rule_result, ai_result)

        return jsonify(final_result), 200
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
    except Exception as error:
        print("NoticeGuard analysis error:", error)
        return jsonify({
            "error": (
                "Unable to analyze the notice. "
                "Please try again."
            )
        }), 500


def build_final_result(rule_result, ai_result):
    if ai_result:
        return {
            "verdict": ai_result.get("verdict", rule_result["verdict"]),
            "confidence": ai_result.get("confidence", rule_result["confidence"]),
            "reasons": ai_result.get("reasons", rule_result["reasons"])
        }
    return {
        "verdict": rule_result["verdict"],
        "confidence": rule_result["confidence"],
        "reasons": rule_result["reasons"]
    }
