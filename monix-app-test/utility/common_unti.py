class CommonUnit:
    @staticmethod
    def is_contain(str1, str2):
        """判断字符串是否包含"""
        flag = None
        if str(str1) in str(str2):
            flag = True
        else:
            flag = False
        return flag

    @staticmethod
    def is_has_key(str1, str2):
        """判断key是否存在"""
        if str1 in str2.keys():
            flag = True
        else:
            flag = False
        return flag

