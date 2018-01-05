import os
import shutil
from conf.settings import web_conf_path


class Manager:
    def __init__(self, server_id, conf_type, version='', select_id=None):
        self.server_id = server_id
        self.conf_type = conf_type
        self.version = version
        self.select_id = select_id
        self.file_root_path = web_conf_path

        # 初始化id 列表
        if not self.select_id:
            self.id_list = []
        else:
            self.id_list = list(map(lambda x: int(x), self.select_id))

    def __check_path(self, id_index=None, path=None):
        if path:
            current_path = path
        else:
            current_path = self.file_root_path + '/%s/%s/%s' % (self.server_id, self.conf_type, self.version)

        if id_index != None:
            file_list = os.listdir(current_path)
            return current_path + '/%s' % file_list[id_index]
        else:
            return current_path

    def __get_last_path(self):
        if self.id_list:
            new_path = None
            for id_index in self.id_list:
                new_path = self.__check_path(id_index, new_path)
            return new_path
        else:
            return self.__check_path()

    def __get_last_version_path(self):
        return self.file_root_path + '/%s/%s/last_version' % (self.server_id, self.conf_type)

    def __compare(self, x, y):
        stat_x = os.stat(self.__get_last_path() + "/" + x)

        stat_y = os.stat(self.__get_last_path() + "/" + y)

        if stat_x.st_ctime < stat_y.st_ctime:
            return -1
        elif stat_x.st_ctime > stat_y.st_ctime:
            return 1
        else:
            return 0

    def __get_dir_itmes(self, dir):
        return os.listdir(dir)

    def __dir_mandatory_check(self, dir, filename):
        return os.path.isdir('%s/%s' % (dir, filename))

    def get_items(self):
        file_list = self.__get_dir_itmes(self.__get_last_path())
        data_list = []
        id_count = 0
        for file in file_list:
            obj_dic = {}
            level_up = ''.join(list(map(str, self.id_list)))
            id_str = str(id_count)
            obj_dic['id'] = level_up + id_str
            obj_dic['name'] = file
            obj_dic['isParent'] = self.__dir_mandatory_check(self.__get_last_path(), file)
            data_list.append(obj_dic)
            id_count += 1

        return data_list

    def create_items(self, name, item_path, item_type):
        try:
            base_dir = self.__get_last_path()
            item_path = '%s%s' %(base_dir, item_path)
            if item_type == 'file':
                with open('%s%s' % (item_path, name), 'w') as f:
                    f.write('')
            elif item_type == 'dir':
                os.makedirs('%s%s' % (item_path, name))
            #os.makedirs('%s/%s' %(base_dir, name))
            return True
        except Exception as e:
            print(Exception, e)
            return False

    def get_file(self):
        file_path = self.__get_last_path()
        f = open(file_path, 'r')
        file_data = f.read()
        f.close()
        return file_data

    def set_to_last_version(self):
        # delete last version first
        source_path = self.__get_last_path()
        target_path = self.__get_last_version_path()
        try:
            shutil.rmtree(target_path)
        except:
            pass

        # copy files
        shutil.copytree(source_path, target_path)
        return True


if __name__ == "__main__":
    my_handle = Manager(None, 56, 'nginx', '2017-12-28-09-08-10')
    print(my_handle.get_items())
