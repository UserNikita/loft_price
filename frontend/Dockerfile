FROM node:16.6.1-alpine3.13

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./

RUN npm install

RUN npm install react-scripts@3.4.1 -g

COPY . ./

CMD ["npm", "start"]
