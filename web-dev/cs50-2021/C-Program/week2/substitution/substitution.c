#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>



int main(int argc, string argv[])
{
 if (argc != 2)
 {
  printf("Usage: ./substitution key\n");
  return 1;
 }

 if (strlen(argv[1]) != 26)
 {
 printf("key must be at least 26 characters. \n");
  return 1;
 }

for (int i = 0; i < strlen(argv[1]); i++)
{
 if(!isalpha(argv[1][i]))
 {
  printf("Only alphabetical keys:\n");
  return 1;
 }
}

char alphabet[2][26];
for (int i = 0; i < strlen(argv[1]); i++)
{
 alphabet[0][i] = 'A' + i;
 alphabet[1][i] = argv[1][i];
}


for (int i = 0; i < strlen(argv[1]); i++)
{
 int j = 0;
 for (int k = 0; k < strlen(argv[1]); k++)
 {
  if (toupper(alphabet[1][k]) == toupper(alphabet[1][i]))
  {
   j++;
   if (j == 2)
   {
    printf("Character is repeated, please check key\n");
    return 1;
   }
  }
 }
}

//finally made it to the algorithm; please recommend something better
string plaintext = get_string("Plaintext: ");
printf("ciphertext: ");
for (int i = 0, j = strlen(plaintext); i < j; i++)
{
 if (isalpha(plaintext[i]))
  {
   if (islower(plaintext[i]))
    {
      for (int k = 0; k < strlen(argv[1]); k++)
       {
        if (tolower(alphabet[0][k]) == plaintext[i])
         {
          printf("%c", tolower(alphabet[1][k]));
         }
       }
    }
   if (isupper(plaintext[i]))
    {
     for (int k = 0; k < strlen(argv[1]); k++)
      {
       if (toupper(alphabet[0][k]) == plaintext[i])
        {
         printf("%c", toupper(alphabet[1][k]));
        }
      }
    }
  }
else
  {
   printf("%c", plaintext[i]);
  }
}
 printf("\n");
 return 0;
}