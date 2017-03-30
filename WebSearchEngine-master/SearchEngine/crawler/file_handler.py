#encoding=utf-8

from SearchEngine.utils import logger

class Data_Handler_Base():
    """
    designed to save data
    """
    def __init__(self):
        pass

    def save_result(result):
        """
        need to be derived to implement
        """
        pass

class Data2File_Handler(Data_Handler_Base):
    """
    save processed data to disk, use csv as default format
    """
    def __init__(self, file_name):
        try:
            self.__file_handler = open(file_name, "wb")
        except IOError:
            logger.error("can not open file <file_name: %s>"%file_name)
            assert False
        else:
            logger.info("create file <filename: %s> to save data"%file_name)

    def save_result(self, result):
        """
        save result to disk
        @param: result should be a dict
        @todo: modify params check
        """
        if isinstance(result, dict):
            result = list().append(result)
        if isinstance(result, list) and \
            len(result) and \
            isinstance(result[0], dict):
            pass
        else:
            logger.warning("no result to be saved")
            # todo: throw a exception
            return
        for dict_item in result:
            for key in dict_item:
                info = dict_item[key].encode("utf-8").replace(",","_")
                self.__file_handler.write("%s,"%info)
            self.__file_handler.write("\n")

    def __del__(self):
        self.__file_handler.close()
