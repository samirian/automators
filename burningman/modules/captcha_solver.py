from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask


class Captcha_Solver:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def solve(self, site_key: str, url: str):
        client = AnticaptchaClient(self.api_key)
        task = NoCaptchaTaskProxylessTask(url, site_key)
        job = client.createTask(task)
        print("getting CAPTCHA solution..")
        job.join()
        return job.get_solution_response()