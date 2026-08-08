const createApp = require('./app');

const PORT = process.env.PORT || 3001;
const app = createApp();

app.listen(PORT, () => {
  console.log(`Campus Manager API listening on http://localhost:${PORT}`); // eslint-disable-line no-console
});
