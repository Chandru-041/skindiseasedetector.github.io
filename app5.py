import io
import os
import base64

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Define the mapping from disease ID to name
disease_map = {
    0: "Actinic keratoses and intraepithelial carcinoma / Bowen's disease",
    1: "Basal cell carcinoma",
    2: "Benign keratosis-like lesions (solar lentigines / seborrheic keratoses and lichen-planus like keratoses)",
    3: "Dermatofibroma",
    4: "Melanoma",
    5: "Melanocytic nevi",
    6: "Vascular lesions"
}

# Load the pre-trained model
model_path = os.path.join(os.getcwd(), 'best_model.h5')
model = load_model(model_path)

# Define the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Skin Disease Classification"),
    dcc.Upload(
        id="upload-image",
        children=html.Div(["Drag and drop or click to select an image to upload."]),
        style={
            "width": "50%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px"
        },
        accept="image/*"
    ),
    html.Div(id="output-image-upload"),
    html.Div(id="output-prediction")
])

# Define the callback function to process the uploaded image and make a prediction
@app.callback(
    [Output("output-image-upload", "children"), Output("output-prediction", "children")],
    [Input("upload-image", "contents")],
    [State("upload-image", "filename"), State("upload-image", "last_modified")]
)
def process_image(contents, filename, last_modified):
    if contents is None:
        return None, None
    # Decode the uploaded image
    content_type, content_string = contents.split(",")
    decoded_image = base64.b64decode(content_string)
    # Load the image using PIL and resize it to match the input shape of the model
    image = Image.open(io.BytesIO(decoded_image))
    image = image.resize((28, 28))
    # Convert the image to a Numpy array and normalize its values
    image = np.array(image)
    image = image.astype("float32") / 255.
    image = np.expand_dims(image, axis=0)
    # Make a prediction using the pre-trained model
    prediction = model.predict(image)
    disease_id = np.argmax(prediction)
    disease_name = disease_map[disease_id]
    # Create an HTML element to display the uploaded image
    image_element = html.Div([
        html.Img(src=contents, style={"width": "50%"}),
        html.Br(),
        html.Span(filename),
        html.Br(),
        html.Span(f"Last modified: {last_modified}")
    ])
    # Create an HTML element to display the prediction result
    prediction_element = html.H2(f"Prediction: {disease_name}")
    return image_element, prediction_element

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
