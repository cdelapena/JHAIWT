```
   _____             .___     .__    ________                     .__                                       __   
  /     \   ____   __| _/____ |  |   \______ \   _______  __ ____ |  |   ____ ______   _____   ____   _____/  |_ 
 /  \ /  \ /  _ \ / __ |/ __ \|  |    |    |  \_/ __ \  \/ // __ \|  |  /  _ \\____ \ /     \_/ __ \ /    \   __\
/    Y    (  <_> ) /_/ \  ___/|  |__  |    `   \  ___/\   /\  ___/|  |_(  <_> )  |_> >  Y Y  \  ___/|   |  \  |  
\____|__  /\____/\____ |\___  >____/ /_______  /\___  >\_/  \___  >____/\____/|   __/|__|_|  /\___  >___|  /__|  
        \/            \/    \/               \/     \/          \/            |__|         \/     \/     \/ 
```
# Description
This is a basic model for recommendations between user data and match data (i.e. from job postings).

## How it works:
1. A complete corpus (i.e. "large body") of text is broken into words (tokenization), the stored as vectors.
2. These vectors are then transformed with a Term Frequency-Inverse Document Frequency (TF-IDF) transformer
analyzing the frequency at which a word appears in the complete document compared to all other words
in the document. 
 !NOTE! This score represents the importance of the word in the document relative to the 
entire collection of documents.

3. By performing a dot product calculation, to check for alignment of the vectors being compared

4. The magnitude of the dot products is then calculated.

5. The cosine similarities algorithm then divides the dot product by the magnitude resulting an a discrete
value between -1 and 1 to assess the alignment of the vectors. This allows us to know how similar or dissimilar
two bodies of text are.

6. The resulting cosine similarities are then ranked with the top_n matches to the user printed back as a result.

## Getting Started...
### To try it out:
- Pull the repo and cd into the test_model folder.
- Create a .venv by running the command `bash build_model_env`
    - This will handle building a python venv (if one is not available)
    - Installing all model dependencies
    - Activating the venv for use
- Run the rank_values.py script with `python rank_values.py`
