class FormMixin(object):
    def get_errors(self):
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data()
            errors_dict = {}
            for key,v in errors.items():
                errors_list = []
                for error_dict in v:
                    message = error_dict["message"]
                    errors_list.append(message)
                errors_dict[key] = errors_list
            return errors_dict
        else:
            return {}