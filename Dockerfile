FROM lambci/lambda:build-python3.6

WORKDIR /var/task

# Fancy prompt to remind you are in zappashell
RUN echo 'export PS1="\[\e[36m\]serverlessml>\[\e[m\] "' >> /root/.bashrc

CMD ["bash"]