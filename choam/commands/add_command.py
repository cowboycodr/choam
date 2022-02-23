from choam.commands.command import Command

class AddCommand(Command):
    def __init__(
        self,
        choam
    ):
        super().__init__(ctx=choam)

    def run(
        self,
        dependency_name: str,
        *args,
        **kwargs,
    ):
        '''
        Add a dependecy to required/dev/ignored modules in
        `Choam.toml`
        '''

        config = self.config.get()

        if kwargs.get("ignore", None):
            config["modules-ignore"][dependency_name] = "*"

            config = self.remove_from_modules(config, dependency_name)

        elif kwargs.get("dev", None):
            if not self.config.is_section("modules-dev"):
                config["modules-dev"] = {}

            config["modules-dev"][dependency_name] = "*"
            config = self.remove_from_modules(config, dependency_name)

        else:
            config["modules"][dependency_name] = "*"

        self.config.set(config)

        if kwargs.get("install", None):
            self.ctx.install()

    def remove_from_modules(self, config: dict, module: str):
        result = config.copy()

        if module in result["modules"].keys():
            result["modules"].pop(module)

        return result