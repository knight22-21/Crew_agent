from crew.job_crew import create_job_crew

if __name__ == "__main__":
    crew = create_job_crew()
    result = crew.kickoff()
    print(result)
