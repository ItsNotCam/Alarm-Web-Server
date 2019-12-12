from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import *
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(BadRequest)
    def handle_bad_request(err):
        return err.message, 400
    
    @app.errorhandler(Unauthorized)
    def handle_unauth(err):
        return err.message, 401
    
    @app.errorhandler(Forbidden)
    def handle_forbidden(err):
        return err.message, 403
    
    @app.errorhandler(NotFound)
    def handle_notfound(err):
        return "", 404
    
    @app.errorhandler(MethodNotAllowed)
    def handle_not_allowed(err):
        return err.message, 405

    @app.errorhandler(TooManyRequests)
    def handle_tmr(err):
        return err.message, 424
    
    @app.errorhandler(InternalServerError)
    def handle_ise(err):
        return err.message, 429
    
    @app.errorhandler(FailedDependency)
    def handle_failed_dependency(err):
        return err.message, 500

    @app.errorhandler(NotImplemented)
    def handle_unimplemented(err):
        return err.message, 501
    
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(401, handle_unauth)
    app.register_error_handler(403, handle_forbidden)
    app.register_error_handler(404, handle_notfound)
    app.register_error_handler(405, handle_not_allowed)
    app.register_error_handler(424, handle_failed_dependency)
    app.register_error_handler(429, handle_tmr)
    app.register_error_handler(500, handle_ise)

    @app.errorhandler(422)
    def handle_validation_error(err):
        headers = err.data.get("headers", None)
        errors = err.data.get("messages", ["unprocessable entity"])

        if errors is not None:
            return jsonify({
                "message": "invalid data in headers",
                "errors": errors
            }), err.code, headers
        
        else:
            return jsonify({
                "message": "unprocessable entity"
            }), err.code, headers
