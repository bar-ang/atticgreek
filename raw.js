import { vInfo } from './vocabdataSecondEdition.js';

const jsonString = JSON.stringify(vInfo, null, 2);  // Pretty print with 2-space indentation

const blob = new Blob([jsonString], { type: 'application/json' });
const url = URL.createObjectURL(blob);

const a = document.createElement('a');
a.href = url;
a.download = 'atticgreek.json';
a.click();

URL.revokeObjectURL(url);  // Clean up
