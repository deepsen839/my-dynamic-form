CREATE USER 'deep'@'host.docker.internal' IDENTIFIED BY 'deep1234';
GRANT ALL PRIVILEGES ON *.* TO 'deep'@'host.docker.internal' WITH GRANT OPTION;
FLUSH PRIVILEGES;