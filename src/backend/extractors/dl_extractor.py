from .base_extractor import BaseExtractor
from .data_models.DL_data_model import DriverLicenseData
from .encode_image import encode_image
import fireworks.client
import glob
import os
from pprint import pprint 

class DLExtractor(BaseExtractor):
    def extract(self, file_path: str):
        encoded_image = encode_image(file_path)
        response = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/llama-v3p2-90b-vision-instruct",
            response_format={"type": "json_object", "schema": DriverLicenseData.model_json_schema()},
            messages = [
            {
        "role": "system",
        "content": [{
            "type": "text",
            "text": f"You are an AI assistant specialized in extracting information from identity documents. \
                Always return your analysis as a valid JSON object without any additional text \
or explanations. \
            This is the schema required for the output: \
            {str(DriverLicenseData.model_json_schema())}"
        } ],
        },
            
        {
        "role": "user",
        "content": [{
            "type": "text",
            "text": f"""
        Analyze the image of the identity document and extract the following information.
        Return a valid JSON object with these fields:
        
          "surname": "Surname of the license holder, located in the field numbered 1, or called LN",
          "given_names": "Given of the license holder, located in the field numbered 2 of the licence, or called FN",
          "date_of_birth": "Date of birth of the license holder, located in the field numbered 3 of the licence or called DOB",
          "date_of_issue": "Date of Issue in YYYY-MM-DD format located in field 4a of the licence",
          "date_of_expiration": "Date of Expiration in YYYY-MM-DD format located in field 4b of the licence or seen as EXP",
          "dl_number": "Driver License Number (DLN) located on field 4d of the licence or called DL",
          "state": "Name of the state that issued the driver's license",
          "address": "Full address of the license holder, located on field 8 of the licence that is at least two lines long",
          "sex": "Sex as listed on the license, located on field 15 of the licence."
        
        The schema is {str(DriverLicenseData.model_json_schema())}""",
        }, {
            "type": "image_url",
            "image_url": {
            "url": encoded_image
            },
        }, ],
        }],
)
        return response.choices[0].message.content


pp_extractor = DLExtractor()

document_path = '../../../identity_documents'
for document in glob.glob(os.path.join(document_path, '*')):
    if 'License' in document:
        pp_extractor.extract(document)

