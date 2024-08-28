from landsatxplore.earthexplorer import EarthExplorer
import os

from Database import Database


def find_object_by_key_value(lst, key, value):
    return next((item for item in lst if item.get(key) == value), None)


class API_download:
    def __init__(self, user, password):
        super().__init__()
        self.ee = EarthExplorer(user, password)
        self.user_api = user
        self.pass_api = password

    def download_scene(self, sorted_scenes, idx, password, db, user, host, port, dir = './data'):
        chosen_scene = find_object_by_key_value(sorted_scenes, 'display_id', idx)
        # output_dir = self.output_dir.text() if self.output_dir.text() else dir
        # print(sorted_scenes)
        # print(idx)
        # print(chosen_scene)
        if chosen_scene:
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            metadata_to_database = Database(password, db, user, host, port)
            print('Downloading started')
            try:
                self.ee.download(chosen_scene['display_id'], output_dir=os.path.join(dir))
            except Exception as e:
                print(f"Error during download: {e}")
                return
            
            print('Downloading ended')

            print('Writing metadata to PSQL')
            try:
                metadata_to_database.save_metadata(chosen_scene)
            except Exception as e:
                print(f"Error during download: {e}")
                return
            print('Writing metadata to PSQL finished')
            self.logout_ee()

    def logout_ee(self):
        self.ee.logout()
        self.api.logout()