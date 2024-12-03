from .base_extractor import BaseExtractor
from .data_models.passport_data_model import PassportData
from .encode_image import encode_image
import fireworks.client
import glob
import os
from pprint import pprint 

class PassportExtractor(BaseExtractor):
    def extract(self, file_path: str):
        encoded_image = encode_image(file_path)
        response = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/llama-v3p2-90b-vision-instruct",
            response_format={"type": "json_object", "schema": PassportData.model_json_schema()},
            messages = [
            {
        "role": "system",
        "content": [{
            "type": "text",
            "text": f"You are an AI assistant specialized in extracting information from identity documents. \
                Always return your analysis as a valid JSON object without any additional text \
or explanations. \
        For passports, include nationality. For driver's licenses, include state. Leave these fields empty if not applicable. \
            This is the schema required for the output: \
            {str(PassportData.model_json_schema())}"
        } ],
        },
            
        {
        "role": "user",
        "content": [{
            "type": "text",
            "text": f"""
        Analyze the image of the identity document and extract the following information.
        Return a valid JSON object with these fields:
        
          "surname": "The surname of the individual from the surname field of the passport",
          "given_names": "The given names of the individual from the given names field of the passport",
          "date_of_birth": "Date of birth in YYYY-MM-DD format from the date of birth field of the passport",
          "date_of_issue": "Date when passport was issued in YYYY-MM-DD format from the date of issue field of the passport",
          "date_of_expiration": "Document expiration date in YYYY-MM-DD format from the date of expiration of the passport",
          "passport_no": "Passport No. from the Passport No. field of the image",
          "nationality": "For passports only from the Nationality field of the image",
          "place_of_birth": "For passports only from the place of birth field of the image",
          "sex": "The sex on the document from the sex field of the image",
          "authority": "Country that issued the passport from the authority field of the passport."
        
        The schema is {str(PassportData.model_json_schema())}""",
        }, {
            "type": "image_url",
            "image_url": {
            "url": encoded_image
            },
        }, ],
        }],
)
        return response.choices[0].message.content


pp_extractor = PassportExtractor()

document_path = '../../../identity_documents'
for document in glob.glob(os.path.join(document_path, '*')):
    if 'passport' in document:
        pp_extractor.extract(document)

