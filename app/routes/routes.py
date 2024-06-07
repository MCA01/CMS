from flask import flash

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from ..services.user_service import UserService

import os

from ..models.user import User
from ..models.author import Author


def start(app, db, bcrypt):
    @app.route("/", methods=["GET", "POST"])
    def index():
        return render_template("index.html")


    @app.route("/register/", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")
        elif request.method == "POST":
            user_name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            user_type = request.form.get("user_type")
            print(f"Debug Info: {user_name}, {email}, {password}, {user_type}")  # Debug statement
            expertise_topic = request.form.get("expertise_topic")
            user = UserService.register_user(user_name, email, password, user_type, expertise_topic)
            if user:
                login_user(user)
                if user.user_type == "reviewer":
                    return redirect(url_for("reviewer_page_index"))
                elif user.user_type == "author":
                    return redirect(url_for("author_page_index"))
            else:
                return redirect(url_for("register"))

    from ..models.reviewer import Reviewer
    @app.route("/sign_in/", methods=["GET", "POST"])
    def sign_in():
        if request.method == "GET":
            return render_template("sign_in.html")
        elif request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            user = UserService.sign_in_user(email, password)
            if user:
                login_user(user)
                if user.user_type == "reviewer":
                    return redirect(url_for("reviewer_page_index"))
                elif user.user_type == "author":
                    return redirect(url_for("author_page_index"))
            else:
                return redirect(url_for("register"))

    from ..services.paper_service import AuthorService

    @app.route("/author_page/")
    @login_required
    def author_page():
        if current_user.user_type == "author":
            papers = AuthorService.get_author_papers(current_user.pid)
            return render_template("author_page.html", papers=papers)


        else:
            return redirect(url_for("sign_in"))

    @app.route("/author_page_index/")
    @login_required
    def author_page_index():
        author = Author.query.filter_by(id=current_user.pid).first()
        return render_template("author_page_index.html", author=author)

    @app.route('/paper_review_page/<int:paper_id>', methods=['GET', 'POST'])
    @login_required
    def paper_review_page(paper_id):
        if request.method == 'GET':
            #paper = Paper.query.get_or_404(paper_id)
            assignment = Assignment.query.filter_by(paper_id = paper_id).first()
            review = Review.query.filter_by(paper_id = paper_id).first()
            return render_template('paper_review_page.html', review = review , assignment = assignment)
        return "Invalid request", 400

    from ..models.assignment import Assignment
    from ..services.review_service import ReviewerService
    @app.route("/reviewer_page/")
    @login_required
    def reviewer_page():
        if current_user.user_type == "reviewer":
            assignments = ReviewerService.get_reviewer_assignments(current_user.pid)
            return render_template('reviewer_page.html', assignments=assignments)
        else:
            return redirect(url_for("index"))

    @app.route("/reviewer_page_index/")
    @login_required
    def reviewer_page_index():
        reviewer = Reviewer.query.filter_by(id=current_user.pid).first()
        return render_template("reviewer_page_index.html", reviewer = reviewer)


    from ..models.paper import Paper
    from ..services import paper_service

    @app.route('/file_upload/', methods=['POST'])
    def file_upload():
        if current_user.user_type != "author":
            return redirect(url_for("index"))

        title = request.form['title']
        topic = request.form['topic']
        file = request.files['file']

        AuthorService.upload_file(current_user.pid, title, topic, file)
        return redirect(url_for("author_page"))

    from ..models.review import Review

    @app.route('/review/<int:paper_id>', methods=['GET', 'POST'])
    @login_required
    def review(paper_id):
        if request.method == 'GET':
            paper = Paper.query.filter_by(paper_id=paper_id).first_or_404()
            return render_template('review.html', paper=paper)

        elif request.method == 'POST':
            score = request.form.get('score')
            comments = request.form.get('comments')
            result = request.form.get('result')
            ReviewerService.ReviewService.submit_review(current_user.pid, paper_id, score, comments,result)
            return redirect(url_for('reviewer_page'))

        return "Invalid request", 400

    @app.route("/sign_out/", methods=["GET", "POST"])
    def sign_out():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/delete/<pid>", methods=["GET"])
    def delete(pid):
        Paper.query.filter(Paper.paper_id == pid).delete()

        db.session.commit()
        return redirect(url_for("view"))

    @app.route("/view/", methods=["GET", "POST"])
    def view():
        people = Paper.query.all()
        return render_template("view.html", people=people)

    """
        @app.route("/sign_out/", methods=["GET", "POST"])
        def sign_out():
            logout_user()
            return redirect(url_for("index"))


        @app.route("/view/", methods=["GET", "POST"])
        def view():
            people = User.query.all()
            return render_template("view.html", people=people)

        @app.route("/view2/", methods=["GET", "POST"])
        def view2():
            reviews = Review.query.all()
            for review in reviews:
                print(f"score : {review.score}, comment : {review.comments}")
            return render_template("view.html", people=reviews)

        @app.route("/view3/", methods=["GET", "POST"])
        def view3():
            people = Assignment.query.all()

            return render_template("view.html", people=people)


        @app.route("/delete/<pid>", methods=["GET"])
        def delete(pid):
            User.query.filter(User.pid == pid).delete()

            db.session.commit()
            return redirect(url_for("view"))
        """
    """
       @app.route('/flist/')
       def file_list():
           files = Paper.query.all()
           return render_template("file_list.html", files=files)
       """
    """
    @app.route("/submit_paper", methods=["GET", "POST"])
    @login_required
    def submit_paper():
        if current_user.user_type != "author":
            return redirect(url_for("index"))
    """
