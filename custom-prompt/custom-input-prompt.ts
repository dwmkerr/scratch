// custom-input-prompt.ts
import { 
  createPrompt, 
  useState, 
  useKeypress, 
  usePrefix, 
  isEnterKey, 
  isBackspaceKey, 
  makeTheme, 
  type Theme, 
  type Status 
} from '@inquirer/core';
import type { PartialDeep } from '@inquirer/type';
import colors from 'colors';

type InputTheme = {
  validationFailureMode: 'keep' | 'clear';
};

const inputTheme: InputTheme = {
  validationFailureMode: 'keep'
};

export type InputConfig = {
  message: string;
  default?: string;
  required?: boolean;
  transformer?: (value: string, options: { isFinal: boolean }) => string;
  validate?: (value: string) => boolean | string | Promise<string | boolean>;
  hint?: string; // our custom hint property
  theme?: PartialDeep<Theme<InputTheme>>;
};

export default createPrompt<string, InputConfig>((config, done) => {
  const { required, validate = () => true } = config;
  const theme = makeTheme<InputTheme>(inputTheme, config.theme);
  const [status, setStatus] = useState<Status>('idle');
  const [defaultValue = '', setDefaultValue] = useState<string>(config.default);
  const [errorMsg, setError] = useState<string>();
  const [value, setValue] = useState<string>('');

  const prefix = usePrefix({ status, theme });

  useKeypress(async (key, rl) => {
    // Ignore keypress if prompt is busy.
    if (status !== 'idle') {
      return;
    }

    if (isEnterKey(key)) {
      const answer = value || defaultValue;
      setStatus('loading');

      const isValid =
        required && !answer ? 'You must provide a value' : await validate(answer);
      if (isValid === true) {
        setValue(answer);
        setStatus('done');
        done(answer);
      } else {
        if (theme.validationFailureMode === 'clear') {
          setValue('');
        } else {
          // Reset the readline line value to the previous value.
          rl.write(value);
        }
        setError(isValid || 'You must provide a valid value');
        setStatus('idle');
      }
    } else if (isBackspaceKey(key) && !value) {
      setDefaultValue(undefined);
    } else {
      // Hook for additional keystroke logic can be added here.
      setValue(rl.line);
      setError(undefined);
    }
  });

  const message = theme.style.message(config.message, status);
  let formattedValue = value;
  if (typeof config.transformer === 'function') {
    formattedValue = config.transformer(value, { isFinal: status === 'done' });
  } else if (status === 'done') {
    formattedValue = theme.style.answer(value);
  }

  let defaultStr: string | undefined;
  if (defaultValue && status !== 'done' && !value) {
    defaultStr = theme.style.defaultAnswer(defaultValue);
  }

  let error = '';
  if (errorMsg) {
    error = theme.style.error(errorMsg);
  }

  // Create the hint string (displayed in grey) only if there's no input.
  let hintStr = '';
  if (!value && config.hint) {
    hintStr = colors.gray(config.hint);
  }

  const lineOutput = [prefix, message, defaultStr, formattedValue]
    .filter((v) => v !== undefined)
    .join(' ');

  // Return the editable prompt (lineOutput) as the first element,
  // and the hint (or error, if present) as the second element.
  return [lineOutput, error || hintStr];
});
