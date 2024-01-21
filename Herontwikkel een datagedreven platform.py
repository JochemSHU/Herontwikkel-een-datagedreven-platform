import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import openai

# Stel je API-sleutel in
openai.api_key = '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'

# Definieer de koppeling tussen geselecteerde opties en complete zinnen
style_options_mapping = {
    "Cartoon": "In de stijl van Cartoon",
    "Realistisch": "In fotografische stijl",
    "Vaporwave": "In de stijl van Vaporwave",
    "Technische tekening": "In de stijl van een Technische tekening",
    "Olieverf": "In de stijl van Olieverf",
    "Impressionistisch": "In de stijl van Impressionisme",
    "Kubisme": "In de stijl van Kubisme",
    "Popart": "In de stijl van Pop Art",
    "Minimalistisch": "In Minimalistische stijl",
    "Abstract": "In Abstracte stijl",
    # Voeg meer stijlen toe indien nodig
}

# Lijst van stijlen voor de tweede dropdown
second_dropdown_styles = {
    "Normaal": "In volledige kleur",
    "Zwart wit": "In zwart-wit",
    "Sepia": "Gebruik sepia-kleuren",
    "Neon": "Gebruik Neon-kleuren",
    "Pastel": "Gebruik Pastel-kleuren",
    "Monochroom": "In Monochroom",
    "Complementaire kleuren": "Gebruik complementaire kleuren",
    # Voeg meer kleurstijlen toe indien nodig
}


# Functie om afbeeldingen te genereren met stijloverdracht
def generate_images(prompt, filters, num_images=2):
    # Combineer filters met de prompt
    prompt_with_filters = f"{prompt} {filters}"
    
    # Doe een verzoek naar de OpenAI Image API
    response = openai.Image.create(
        prompt=prompt_with_filters,
        n=num_images,
        size="1024x1024"
    )

    # Haal de URL's op uit de API-respons
    image_urls = [result['url'] for result in response['data']]
    return image_urls

def main():
    st.title("Pixel Wizards")
    st.title("Generator")

    # Invoer voor de afbeeldingsprompt
    image_prompt = st.text_input("Voer je afbeeldingsprompt in, moet in het engels!:", "")
    
    # Zijbalk met dropdowns en tekstinvoer voor filters
    with st.sidebar:
        st.header("Filters voor de afbeeldingen")
        filter1 = st.selectbox("Stijl van de afbeelding", list(style_options_mapping.keys()))
        filter2 = st.selectbox("Kleurgebruik", list(second_dropdown_styles.keys()))
        #additional_filter_text = st.text_input("Vul hier in wat je niet wilt zien, moet in het engels!", "")

    if st.button("Genereer Afbeeldingen"):
        if image_prompt:
            # Koppel geselecteerde opties aan complete zinnen
            selected_filter1 = style_options_mapping.get(filter1, filter1)
            selected_filter2 = second_dropdown_styles.get(filter2, filter2)
            selected_filters = f"{selected_filter1} {selected_filter2}"
            #{additional_filter_text}"

            # Genereer afbeeldingen met stijloverdracht
            generated_image_urls = generate_images(image_prompt, selected_filters)

            st.subheader("Gegenereerde Afbeeldingen:")

            # Toon twee afbeeldingen naast elkaar
            columns = st.columns(2)
            for i, (column, image_url) in enumerate(zip(columns, generated_image_urls)):
                # Download de afbeelding
                image_response = requests.get(image_url)
                image = Image.open(BytesIO(image_response.content))

                # Toon afbeeldingen in de kolommen
                column.image(image, caption=f"Gegenereerde Afbeelding {i+1}", use_column_width=True)
        else:
            st.warning("Voer eerst je afbeeldingsprompt in.")

if __name__ == "__main__":
    main()

