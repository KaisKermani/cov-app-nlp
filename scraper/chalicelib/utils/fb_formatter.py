from datetime import datetime, timedelta


def format_post_id(link):
    return link.split('permalink/')[1].split('/')[0]


def format_profile_id(link):
    return link.split("facebook.com/")[1].split('groupid')[0].split('profile.php?id=')[-1].split('?')[0].split('&')[0]


def format_extract_time(ts):
    return datetime.strptime(ts, '%a %b %d %H:%M:%S %Y').strftime("%Y-%m-%d %H:%M:%S")


def format_post_time(ts, extract_time):
    try:
        formatted = datetime.strptime(ts, '%d %B at %H:%M')
        extract = datetime.strptime(extract_time, '%Y-%m-%d %H:%M:%S')
        formatted = formatted.replace(year=extract.year)
        return formatted.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            formatted = datetime.strptime(ts, '%d %B %Y at %H:%M').strftime("%Y-%m-%d %H:%M:%S")
            return formatted
        except ValueError:
            pass
    extract = datetime.strptime(extract_time, '%Y-%m-%d %H:%M:%S')
    if ts == 'Just now':
        return extract_time
    try:
        elts = ts.split(' ')
        if 'min' in elts or 'mins' in elts:
            return (extract - timedelta(minutes=int(elts[0]))).strftime("%Y-%m-%d %H:%M:%S")

        elif 'hr' in elts or 'hrs' in elts:
            return (extract - timedelta(hours=int(elts[0]), minutes=30)).strftime("%Y-%m-%d %H:%M:%S")

        elif 'Yesterday' in elts:
            day = extract - timedelta(days=1)
            formatted = datetime.strptime(ts, 'Yesterday at %H:%M')
            formatted = formatted.replace(day=day.day, month=day.month, year=day.year)
            return formatted.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return extract_time