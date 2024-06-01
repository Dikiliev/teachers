from datetime import datetime


class IntListConverter:
    regex = '(-?\d+(,-?\d+)*)?'

    def to_python(self, value: str) -> [int]:
        return [int(item) for item in value.split(',')]

    def to_url(self, value: [int]) -> str:
        return ','.join(str(item) for item in value)


class DateTimeConverter:
    regex = '\d{4}-\d{2}-\d{2}_\d{2}-\d{2}'

    def to_python(self, value: str) -> datetime:
        return datetime.strptime(value, '%Y-%m-%d-%H-%M')

    def to_url(self, value: datetime) -> str:
        return value.strftime('%Y-%m-%d-%H-%M')
