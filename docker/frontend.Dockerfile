FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY public ./public
COPY css ./public/css
COPY js ./public/js
EXPOSE 3000
CMD ["npx", "serve", "public", "-l", "3000"]
