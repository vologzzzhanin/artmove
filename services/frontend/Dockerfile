FROM node:lts-alpine

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package.json .
COPY package-lock.json .

RUN npm install

CMD ["npm", "run", "dev"]
