import nltk

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
lemmatizer = WordNetLemmatizer()
string = '''UiPath.Core.SelectorNotFoundException: Could not find the UI element corresponding to this selector:
<webctrl css-selector='body&gt;body&gt;div&gt;div&gt;form&gt;div&gt;div&gt;div&gt;div&gt;div' tag='DIV'/>

   at UiPath.Core.Activities.ScopeActivity.OnFaulted(NativeActivityFaultContext faultContext, Exception propagatedException, ActivityInstance propagatedFrom)
   at System.Activities.Runtime.FaultCallbackWrapper.Invoke(NativeActivityFaultContext faultContext, Exception propagatedException, ActivityInstance propagatedFrom)
   at System.Activities.Runtime.FaultCallbackWrapper.FaultWorkItem.Execute(ActivityExecutor executor, BookmarkManager bookmarkManager)
this message type in callback:  <class 'str'>
 [x] Done
'''

def lemmatize_word(text):
    word_tokens = word_tokenize(text)
    # provide context i.e. part-of-speech
    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in word_tokens]
    return lemmas

# if __name__ == '__main__':
#     print(lemmatize_word(string.splitlines()[]))

