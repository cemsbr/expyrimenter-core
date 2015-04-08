class Runnable:
    def __init__(self):
        self.title = None
        self.executed = False
        self.output = None
        self.failed = True

    def run(self):
        raise NotImplementedError('Runnable.run not implemented')

    def log(self, logger, extra_msgs=None):
        msgs = []
        if self.title and self.executed:
            msgs.append('finished {}'.format(self.title))

        if extra_msgs:
            msgs.extend(extra_msgs)
        if self.output:
            msgs.append('output "{}"'.format(self.output))

        full_msg = ', '.join(msgs) + '.'
        logger.error(full_msg) if self.failed else logger.info(full_msg)

    def __str__(self):
        string = 'runnable'
        if self.title:
            string += ' "{}"'.format(self.title)
        if not self.executed:
            string += ' not executed.'
        else:
            string += ' executed '
            string += 'with error' if self.failed else 'successfully'
            if self.output:
                string += ', output was "{}".'.format(self.output)

        return string
