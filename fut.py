from flask import Flask, render_template, request, redirect, url_for, flash
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # flash mesajları için gereklidir

# Sorular ve görseller
questions = [
    {"question": "Hangi takım 2020 Süper Lig şampiyonudur?", "image": "../static/img/galatasaray.jpg", "answers": ["Beşiktaş", "Fenerbahçe", "Galatasaray", "Trabzonspor"], "correct": "Galatasaray"},
    {"question": "2021'de en fazla gol atan futbolcu kimdir?", "image": "../static/img/burak_yilmaz.jpg", "answers": ["Burak Yılmaz", "Cenk Tosun", "Vedat Muriqi", "Haris Seferovic"], "correct": "Burak Yılmaz"},
    {"question": "Süper Lig'de en fazla şampiyonluk yaşayan Türk futbolcu kimdir?", "image": "../static/img/şampiyon.jpg", "answers": ["Mario Gomez", "Bafetimbi Gomis", "Hasan Şaş", "Robin Van Persie"], "correct": "Hasan Şaş"},
    {"question": "Süper Lig tarihinin en hızlı golü kimin tarafından atılmıştır?", "image": "../static/img/fast.jpg", "answers": ["Kalu Uche", "Onyekuru", "Kuyt", "Aboubakar"], "correct": "Kalu Uche"},
    {"question": "Süper Lig tarihinin en hızlı golünü atan oyuncu kimdir?", "image": "../static/img/kronometre.jpg", "answers": ["Metin Tekin", "Burak Yılmaz", "Guti", "Pepe"], "correct": "Metin Tekin"},
    {"question": "Süper Lig 1959 yılında kurulduğunda ilk şampiyon olan takım hangisidir?", "image": "../static/img/kupa.jpeg", "answers": ["Trabzonspor", "Fenerbahçe", "Galatasaray", "Beşiktaş"], "correct": "Fenerbahçe"},
    {"question": "2015 yılında oynanan Fenerbahçe – Galatasaray derbisinin skoru nedir?", "image": "../static/img/fbgs.jpg", "answers": ["1-1", "2-0 Fenerbahçe", "2-1 Galatasaray", "3-2 Fenerbahçe"], "correct": "2-0 Fenerbahçe"},
    {"question": "2019 yılında Galatasaray'ın en fazla gol atan oyuncusu kimdir?", "image": "../static/img/galatasaraylogo.jpg", "answers": ["Radamel Falcao", "Henry Onyekuru", "Diagne", "Sofiane Feghouli"], "correct": "Diagne"},
    {"question":"Süper Lig'de 2019 yılında en fazla asist yapan oyuncu kimdir?","image":"../static/img/pas.jpg","answers":["Arda Turan","Gökhan Töre","Henry Onyekuru","Sofiane Feghouli"],"correct":"Henry Onyekuru"},
    {"question":"Süper Lig tarihindeki en büyük farkla galip gelen takım hangisidir?","image":"../static/img/skor.jpg","answers":["Galatasaray","Fenerbahçe","Beşiktaş","Trabzonspor"],"correct":"Beşiktaş"},
    {"question":"Süper Lig tarihinde 3 büyükler dışında şampiyon olan ilk takım kimdir? (2000 sonrası)","image":"../static/img/şamp.jpg", "answers":["Bursaspor","Trabzonspor","Başakşehir","Konyaspor"],"correct":"Bursaspor"},
    {"question":"2021-2022 sezonunda Trabzonspor kaç yıl sonra şampiyon oldu?","image":"../static/img/ts.jpg","answers":["29","38","41","35"],"correct":"38"},
    {"question":"2008-2009 sezonunda Fenerbahçe’nin teknik direktörü kimdi?","image":"../static/img/iso.jpg","answers":["Zico","Luis Aragones","Christoph Daum"," Ersun Yanal"],"correct":"Luis Aragones"},
    {"question":"2020-2021 sezonu gol kralı kimdir?","image":"../static/img/gol.jpg","answers":["Aaron Boupendza","Mbwana Samatta","Vincent Aboubakar","Enner Valencia"],"correct":"Aaron Boupendza"},
    {"question":"2015-2016 sezonunda Süper Lig'e şampiyon olarak yükselen takım hangisidir?","image":"../static/img/sportoto.jpeg","answers":["Osmanlıspor","Alanyaspor","Adanaspor","Kayserispor"],"correct":"Adanaspor"},
    {"question":"Süper Lig’de 2008-2009 sezonunda son haftada şampiyonluğu kaçıran takım hangisidir?","image":"../static/img/defeat.jpg","answers":["Beşiktaş","Trabzonspor","Fenerbahçe","Sivasspor"],"correct":"Sivasspor"},
    {"question":"Süper Lig'de 2000-2023 arasında 3 farklı takımda şampiyonluk yaşamış Türk teknik direktör kimdir?","image":"../static/img/kup.jpg","answers":["Şenol Güneş","Mustafa Denizli","Ersun Yanal","Okan Buruk"],"correct":"Mustafa Denizli"},
    {"question":"2000 yılından sonra Süper Lig’de en fazla maç yöneten hakem kimdir?","image":"../static/img/hakem.jpg","answers":["Cüneyt Çakır","Fırat Aydınus","Bülent Yıldırım","Halil Umut Meler"],"correct":"Cüneyt Çakır"},
    {"question":"Fenerbahçe’nin 2020 yılında Lazio’dan transfer ettiği golcü oyuncu kimdir?","image":"../static/img/fener.jpg","answers":["Muriqi","Valencia","Serdar Dursun","Samatta"],"correct":"Samatta"},
    {"question":"“Devler Ligi Marşı”nın ilk kez Süper Lig'de çaldığı takım hangisidir?","image":"../static/img/tribün.jpg","answers":["Beşiktaş","Fenerbahçe","Galatasaray","Trabzonspor"],"correct":"Galatasaray"},
    # Diğer soruları buraya ekleyebilirsiniz
]

@app.route('/')
def index():
    return redirect(url_for('question', question_number=0, correct_answers=0, incorrect_answers=0))

@app.route('/question/<int:question_number>/<int:correct_answers>/<int:incorrect_answers>', methods=['GET', 'POST'])
def question(question_number, correct_answers, incorrect_answers):
    if question_number >= len(questions):
        return redirect(url_for('result', correct_answers=correct_answers, incorrect_answers=incorrect_answers))

    current_question = questions[question_number]

    if request.method == 'POST':
        selected_answer = request.form['answer']
        if selected_answer == current_question['correct']:
            flash("Doğru Cevapladınız!", 'success')  # Doğru cevap
            correct_answers += 1
        else:
            flash("Yanlış Cevap Üzgünüm", 'error')  # Yanlış cevap
            incorrect_answers += 1
        
        # 1 saniye bekledikten sonra bir sonraki soruya git
        time.sleep(1)
        return redirect(url_for('question', question_number=question_number + 1, correct_answers=correct_answers, incorrect_answers=incorrect_answers))
    
    return render_template('question.html', question=current_question, question_number=question_number, correct_answers=correct_answers, incorrect_answers=incorrect_answers)

@app.route('/result/<int:correct_answers>/<int:incorrect_answers>')
def result(correct_answers, incorrect_answers):
    return render_template('result.html', correct_answers=correct_answers, incorrect_answers=incorrect_answers)

if __name__ == '__main__':
    app.run(debug=True)
