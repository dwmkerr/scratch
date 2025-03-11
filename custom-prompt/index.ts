#!/usr/bin/env ts-node
import inquirer from 'inquirer';
import customInputPrompt from './custom-input-prompt';

// Cast customInputPrompt as any to satisfy registerPrompt’s legacy constructor type.
inquirer.registerPrompt('custom-input', customInputPrompt as any);

// Cast the question array as any to bypass question type conflicts.
const questions: any = [
  {
    type: 'custom-input',
    name: 'userInput',
    message: 'Enter input:',
    hint: '<Enter> Show Menu',
    required: true,
    validate: (input: string) => input.trim() !== '' || 'Input cannot be empty'
  }
];

inquirer
  .prompt(questions)
  .then((answers: any) => {
    console.log('Your input:', answers.userInput);
  });
