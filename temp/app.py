from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def community():
    # 模拟的文章数据
    articles = [
        {'id': 1, 'author': '张三', 'date': '2023-06-22', 'url': 'http://example.com/article1', 'title': '文章一'},
        {'id': 2, 'author': '李四', 'date': '2023-06-23', 'url': 'http://example.com/article2', 'title': '文章二'},
        # 可以继续添加更多的数据
    ]
    return render_template('community1.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)