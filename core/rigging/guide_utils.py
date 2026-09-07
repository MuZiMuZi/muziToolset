

class Guide(object):
    package_dir = os.path.dirname (os.path.abspath (__file__))

    face_guide_template_file_name = "face_guide.ma"
    face_guide_template_path = os.path.join (
        package_config.resources_dir ,
        face_guide_template_file_name
    )

    def __init__(self):
        self.guide_root_name = "grp_md_face_guide_001"
        self.guide_root = None

    def import_template(self,module):
        """
        决定要导入哪个模块的定位器
        """
        cmds.file (face_guide_template_path , i = True , rnn = True)

        pass

    def get_guides(self):
        pass