from flask import Blueprint,render_template
errors=Blueprint('errors',__name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errorPages/404.html',title="404 - Page Not Found"),404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errorPages/403.html',title="403 - UnAuthorized"),403


@errors.app_errorhandler(405)
def error_405(error):
    return render_template('errorPages/405.html',title="405 - Method Error"),405

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errorPages/500.html',title="500 - Server Error"),500