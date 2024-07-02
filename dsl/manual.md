Below are the commands for the FSMIPR DSL

# Load
Usage: `LOAD <filename> AS <variablename>`

Reads the file specified and attempts to interpret the contents. Stores the resulting FA in the variable name specified.

## On Success
If the FSMIPR can interpret the contents of the file (.txt or .json only), the program will respond with
``` Loaded the <FA> contained in <filename> as <variablename> ```
The contents of the file must specify what type of FA it is (e.g. DFA, NFA, TM, etc.) or the file comprehension will fail. For confirmation, the program will tell the user what type of FA it thinks the data structure is.

## Errors
### Malformed Command
If there is no `AS` keyword separating the filename and the variable name, the program will throw a MalformedCommand error
### File Not Found
If the file specified in `<filename>` is not found in the directory where the program is running, the program will throw a FileNotFound error.
### Insufficient Permissions
If the program does not have the required read permissions for `<filename>`, the program will throw an InsufficientPermissions error.
### Type Not Specified
A required field for the contents of the file is `type`, which specifies what type of FA is contained in the document. The list of acceptable FAs can be found in the "Acceptable FAs" section of this manual. If there is no `type` field, the program will throw a TypeNotSpecified error.
### Type Not Recognized
If the `type` field is specified in the file, but is not one of the acceptable FAs contained in the "Acceptable FAs" section of this manual, the program will throw a TypeNotRecognized error.
### Invalid Formatting
Based on the type specified in the `type` field, the program will expect certain fields to be present. For the specific fields required for each type of FA, see the corresponding section for that FA in this manual. If any field cannot be interpreted or is not present, the program will throw an InvalidFormatting error. The error may go into more detail on where the formatting was incorrect, but this is not guaranteed.
### InvalidFA
If the formatting of the file is correct and the program can parse each part of it, but there is some irreconcilable inconsistency contained within, the program will throw an InvalidFA error.

