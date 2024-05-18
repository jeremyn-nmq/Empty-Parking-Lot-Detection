const dotenvExpand = require("dotenv-expand");

dotenvExpand.expand({ parsed: { ...process.env } });

/**
 * @type {import('next').NextConfig}
 */
module.exports = {
  reactStrictMode: true,
  env:{
    NEXT_PUBLIC_BASE_API_URL : process.env.NEXT_PUBLIC_BASE_API_URL
  }
};
