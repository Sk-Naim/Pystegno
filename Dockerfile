FROM python:3.10-slim

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary folders so they don't cause permission errors at runtime
RUN mkdir -p uploads output

# Inform Docker that the container is listening on port 7860
EXPOSE 7860

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
