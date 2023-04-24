import replicate
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Settings

app = FastAPI()
setting = Settings()

# Set the API token
api_token = setting.API_TOKEN
model_version = setting.MODEL_VERSION

# create a replicate client to set the api token
client = replicate.Client(api_token=api_token)

model = client.models.get("stability-ai/stable-diffusion")
version = model.versions.get(
    model_version)

# add CORS middleware
origins = ["http://localhost:3000", "https://music-ai.vercel.app/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Health_Check": "Ok"}


@app.get("/generate-image/{prompt}")
def generate_image(prompt: str):
    inputs = {
        # Input prompt
        'prompt': prompt,

        # pixel dimensions of output image
        'image_dimensions': "768x768",

        # Specify things to not see in the output
        # 'negative_prompt': ...,

        # Number of images to output.
        # Range: 1 to 4
        'num_outputs': 1,

        # Number of denoising steps
        # Range: 1 to 500
        'num_inference_steps': 50,

        # Scale for classifier-free guidance
        # Range: 1 to 20
        'guidance_scale': 7.5,

        # Choose a scheduler.
        'scheduler': "DPMSolverMultistep",

        # Random seed. Leave blank to randomize the seed
        # 'seed': ...,
    }

    output = version.predict(**inputs)

    # Return the AI-generated image
    return {"image": output[0]}
