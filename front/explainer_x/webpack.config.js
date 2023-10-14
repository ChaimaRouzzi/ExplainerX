import { resolve as _resolve } from 'path';

export const entry = './src/index.js';
export const output = {
    path: _resolve(__dirname, 'dist'),
    filename: 'bundle.js', // Output filename
};
export const resolve = {
    fallback: {
        "stream": false
    }
};