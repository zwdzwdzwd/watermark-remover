from flask import Flask, render_template, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["OPTIONS", "GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# 增加上传文件大小限制
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 设置为 50MB

import os
from werkzeug.utils import secure_filename
from watermark_remover import remove_watermark
import tempfile
from pdf2image import convert_from_path
from docx2pdf import convert
from pathlib import Path
from PyPDF2 import PdfMerger
import img2pdf
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return '没有选择文件', 400
    
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件', 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, filename)
        file.save(input_path)
        
        file_ext = filename.rsplit('.', 1)[1].lower()
        output_path = os.path.join(temp_dir, f'output.{file_ext}')
        
        try:
            if file_ext in ['pdf']:
                # 处理所有PDF页面
                pages = convert_from_path(input_path)
                processed_images = []
                
                for i, page in enumerate(pages):
                    # 保存每一页为临时图片
                    temp_img = os.path.join(temp_dir, f'temp_{i}.jpg')
                    page.save(temp_img, 'JPEG')
                    # 处理水印
                    remove_watermark(temp_img, temp_img)
                    processed_images.append(temp_img)
                
                # 将处理后的图片合并为PDF
                with open(output_path, "wb") as f:
                    f.write(img2pdf.convert(processed_images))
                    
            elif file_ext in ['doc', 'docx']:
                # 先转换为PDF
                pdf_path = os.path.join(temp_dir, 'temp.pdf')
                try:
                    convert(input_path, pdf_path)
                    if not os.path.exists(pdf_path):
                        raise Exception("PDF conversion failed")
                        
                    # 处理所有页面
                    pages = convert_from_path(pdf_path)
                    processed_images = []
                    
                    for i, page in enumerate(pages):
                        temp_img = os.path.join(temp_dir, f'temp_{i}.jpg')
                        page.save(temp_img, 'JPEG')
                        remove_watermark(temp_img, temp_img)
                        processed_images.append(temp_img)
                    
                    # 转换回PDF并保存
                    with open(output_path, "wb") as f:
                        f.write(img2pdf.convert(processed_images))
                except Exception as e:
                    print(f"Error converting document: {str(e)}")
                    return '文档转换失败', 500
            else:
                # 图片文件直接处理
                remove_watermark(input_path, output_path)
            
            return send_file(output_path, as_attachment=True, 
                            download_name=f'processed_{filename}')
        except Exception as e:
            print(f"Processing error: {str(e)}")
            return '处理文件时出错', 500
    
    return '不支持的文件类型', 400

if __name__ == '__main__':
    app.run(debug=True, port=9000)  # 使用 9000 端口