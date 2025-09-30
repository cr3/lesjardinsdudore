ARG NODE_VERSION=22
FROM node:${NODE_VERSION}-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile

COPY . ./
RUN npm run build

FROM node:${NODE_VERSION}-alpine AS dev

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile

COPY . ./

EXPOSE 3000
CMD ["npm", "run", "start"]

FROM nginx:alpine AS prod

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 3000 3443
CMD ["nginx", "-g", "daemon off;"]
