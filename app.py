from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from config import app  # Importing main app
from config import api  # Importing api builder

from resources import MeassureDistance

from functions import coors_handle


@app.after_request
def after_request(response: dict) -> dict:
    """
    Function: after_request
    Summary: Prevent COORS problems
    """
    return coors_handle(response)


api.add_resource(MeassureDistance, '/', '/distance/')

# Adding Swagger docs
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Distance to MKAD',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/docs/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/docs-ui/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)  # Init docs
docs.register(MeassureDistance)  # Add endpoints to doc
