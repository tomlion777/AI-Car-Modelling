import numpy as np
import trimesh
import random
import openai

def generate_low_poly_model(prompt, subdivisions=2, radius=1.0, output_file='low_poly.glb'):
    # Use OpenAI API to interpret prompt and determine shape
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You generate parameters for 3D models based on prompts."},
                  {"role": "user", "content": prompt}]
    )
    shape = response["choices"][0]["message"]["content"].strip().lower()
    
    if "sphere" in shape:
        model = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
    elif "cube" in shape:
        model = trimesh.creation.box(extents=[radius, radius, radius])
    elif "cylinder" in shape:
        model = trimesh.creation.cylinder(radius=radius, height=radius*2)
    elif "car" in shape:
        model = trimesh.creation.box(extents=[radius * 2, radius, radius / 2])  # Basic car body
        wheels = [trimesh.creation.cylinder(radius=radius / 4, height=radius / 2) for _ in range(4)]
        for i, wheel in enumerate(wheels):
            wheel.apply_translation([
                (-radius if i % 2 == 0 else radius), 
                (-radius / 2 if i < 2 else radius / 2), 
                -radius / 2
            ])
            model = model + wheel
    else:
        raise ValueError("Unsupported shape")
    
    # Randomly perturb vertices to create a low-poly effect
    perturbation = (np.random.rand(*model.vertices.shape) - 0.5) * 0.1
    model.vertices += perturbation
    
    # Export the model
    model.export(output_file)
    print(f"Low-poly model generated from prompt '{prompt}' and saved as {output_file}")
    
    return output_file

if __name__ == "__main__":
    prompt = input("Enter a description for your 3D model: ")
    generate_low_poly_model(prompt)
