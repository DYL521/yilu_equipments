from equipment.const import ManufactureList


class ExternalAPIBase(object):
    """所有客控厂商API封装的基类。

    对其他模块提供的方法统一命名为 provide_{device_type}_{action} 的形式
    其中 device_type 是 equipment.EquipmentCommon 的某一个子类的类名的小写
    action 可以随便命名.

    处理回调函数的方法统一命名为 receiver_{name} 的形式。因为厂家通常多个设备会调用同一个回调函数，所以这里不再区分
    device_type。通常就可以命名为 receiver_main。如果厂家会调用我们多个API/函数，可以用 name 区分。生产的URL形式为
    /receiver/{manufacture}/{name}

    具体可以参考 external_api.dummy 里面的例子。不符合这两个格式的方法可以作为内部方法使用。

    注意本类的子类不能直接操作 EquipmentCommon 的子类。回调函数处理时如果需要，可以发 Signal， 然后在 Signal 的处理函数
    中操作。Signal 的处理函数应该尽量保持和厂商无关。
    """
    class meta:
        abstract = True

    MANUFACTURE = ""


class ExternalAPIManager(object):
    def __init__(self):
        self.provided_functions = {}  # {manufacture: {device: [action1, action2]}, ..}
        self.receiver_functions = {}  # {manufacture: [action1, action2], ..}
        for api in ExternalAPIBase.__subclasses__():
            if len(api.MANUFACTURE) == 0:
                raise SyntexError("Class {} doesn't have a MANUFACTURE defined".format(api))
            self.provided_functions[api.MANUFACTURE] = {"__api_class__": api}
            self.receiver_functions[api.MANUFACTURE] = {"__api_class__": api, "names": []}

            for attr in api.__dict__:
                if attr.startswith("provide_"):
                    try:
                        device_type = attr.split("_")[1]
                        action = "_".join(attr.split("_")[2:])

                        if device_type in self.provided_functions[api.MANUFACTURE]:
                            self.provided_functions[api.MANUFACTURE][device_type].append(action)
                        else:
                            self.provided_functions[api.MANUFACTURE][device_type] = [action, ]
                    except IndexError:
                        pass

                if attr.startswith("receiver_"):
                    try:
                        name = '_'.join(attr.split("_")[1:])
                        self.receiver_functions[api.MANUFACTURE]['names'].append(name)
                    except IndexError:
                        pass

    def call(self, manufacture_id, device_type, device_id, action, **kwargs):
        try:
            manufacture = ManufactureList.get_choice(manufacture_id).label
        except KeyError:
            raise NotImplementedError("Manufacture ID {} does not exist".format(manufacture_id))

        if manufacture not in self.provided_functions:
            raise NotImplementedError("Manufacture {} does not exist".format(manufacture))

        if device_type not in self.provided_functions[manufacture]:
            raise NotImplementedError("Device {} from manufacture {} does not exist".format(device_type, manufacture))

        if action not in self.provided_functions[manufacture][device_type]:
            raise NotImplementedError("Action {} for Device {} from manufacture {} does not exist".format(
                action, device_type, manufacture))

        function_name = "provide_{}_{}".format(device_type, action)
        api = self.provided_functions[manufacture]["__api_class__"]()
        func = getattr(api, function_name)
        return func(device_id, **kwargs)
