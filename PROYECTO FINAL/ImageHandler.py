#imagehandler 
import pymongo
from bson import Binary
import base64
import os
import random



class ImageHandler:
    def __init__(self, database_name='imgrandom', collection_name='images', connection_string='mongodb://localhost:27018/'):
        self.client = pymongo.MongoClient(connection_string)
        self.database_name = database_name
        self.collection_name = collection_name
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.next_image_id = 1

        if self.collection.count_documents({}) > 0:
            latest_image_id = self.collection.find().sort("_id", -1).limit(1)[0]['_id']
            self.next_image_id = hash(str(latest_image_id)) % (10 ** 8)

    def insert_image(self, file_storage):
        try:
            encoded_image = base64.b64encode(file_storage.read())
            binary_data = Binary(encoded_image)
            result = self.collection.insert_one({'_id': self.next_image_id, 'image': binary_data})
            self.next_image_id += 1
            return result.inserted_id
        except Exception as e:
            print(f'Error uploading image: {e}')
            return None

    def get_image(self, image_id):
        document = self.collection.find_one({'_id': image_id})
        if document:
            encoded_image = document['image']
            decoded_image = base64.b64decode(encoded_image)
            return decoded_image
        else:
            return None

    def get_all_images_base64(self):
        all_images = []
        documents = self.collection.find()
        for document in documents:
            image_id = document['_id']
            encoded_image = document['image']
            decoded_image = base64.b64decode(encoded_image)
            base64_data = base64.b64encode(decoded_image).decode('utf-8')
            all_images.append({'image_id': image_id, 'base64_data': base64_data})
        return all_images

    def delete_image_by_id(self, image_id):
        try:
            result = self.collection.delete_one({'_id': image_id})
            return result.deleted_count
        except Exception as e:
            print(f'Error eliminando la imagen: {e}')
            return 0

    def decode_images(self):
        images = self.get_all_images_base64()
        for image in images:
            image_id = image['image_id']
            image_data = self.get_image(image_id)
            if image_data:
                image_path = os.path.join(self.temp_folder, f'{image_id}.jpg')
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data)

    def get_random_image_base64(self):
        # Obtén el conteo total de documentos en la colección
        count = self.collection.count_documents({})
        if count > 0:
            # Genera un índice aleatorio
            random_index = random.randint(0, count - 1)
            # Encuentra la imagen en la posición aleatoria
            image_data = self.collection.find().skip(random_index).limit(1)[0]
            # Retorna la cadena base64 de la imagen
            return image_data['base64']
        else:
            return None
            
            
            

