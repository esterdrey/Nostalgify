from flask import Flask, render_template

# יצירת אובייקט Flask
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

# רוט להצגת עמוד הבית
@app.route('/')
def home():
    return render_template('index.html')

# הפעלת השרת
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
