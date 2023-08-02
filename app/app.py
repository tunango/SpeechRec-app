import os
from flask import Flask, render_template, request
import speech_recognition as sr

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return "ファイルがアップロードされていません。"
    
    file = request.files['file']

    if file.filename == '':
        return "ファイルが選択されていません。"
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        recognizer = sr.Recognizer()

        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)

        try:
            transcription = recognizer.recognize_google(audio, language='ja-JP')
            return render_template('index.html', transcription=transcription)
        except sr.UnknownValueError:
            return "音声を文字起こしできませんでした。"
        except sr.RequestError as e:
            return f"Google Speech Recognition API エラー: {e}"
        finally:
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)
