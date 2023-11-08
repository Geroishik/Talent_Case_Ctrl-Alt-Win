program Reraite;
const
   n = 3; {От скольки совпадающий в паре предложений слов пара выведится пользователю}
type
   tItem = record
      key: string; {Слово}
      data: set of integer; {В каких предложениях он встречается}
   end; 
var
   f: text;
   Table: array of tItem;
   count, pos, i, j: integer;
   s, w: string; 
   Sentences: array of string; {Массив предложений}
   a: array [,] of integer; {Массив количества совпадающих слов в паре предложений}

{Процедуры добавления в массив}
procedure ArrayAppendItem(var a: array of tItem; NewEl: tItem);
begin
   SetLength(a, Length(a) + 1);
   a[High(a)] := NewEl;
end;

procedure ArrayAppendString(var a: array of string; NewEl: string);
begin
   SetLength(a, Length(a) + 1);
   a[High(a)] := NewEl;
end;

{Линейный поиск в таблице}
procedure LineSearch(var T: array of tItem; K: string; var Res: integer);
var
   i: integer;
begin
   i := Length(T) - 1;
   while (i > -1) and (K <> T[i].key) do
      i := i - 1;
   Res := i;
end;  

{Включение элемента в таблицу}
procedure Add2Table(var T: array of tItem; K: string);
var
   index: integer;
begin
   LineSearch(T, K, index);
   if index = -1 then begin
      ArrayAppendItem(T, new tItem);
      T[High(T)].key := K;
      Include(T[High(T)].data, count);
   end
   else
      Include(T[index].data, count);
end;

{Процедуры для слов}
function isFirstChar(ch: char): Boolean;
begin
   isFirstChar := (ch >= 'а') and (ch <= 'я') or
      (ch >= 'А') and (ch <= 'Я') or
      (ch = 'ё') or (ch = 'Ё') or
      (ch >= 'a') and (ch <= 'z') or
      (ch >= 'A') and (ch <= 'Z')
end;

function isWordChar(ch: char): Boolean;
begin
   isWordChar := isFirstChar(ch) or (ch = '-');
end;

function isLastChar(ch: char): Boolean;
begin
   isLastChar := isFirstChar(ch);
end;

procedure GetWord(s: string; var pos: integer; var w: string);
var
   i: integer; 
begin
   w := '';
   if s <> '' then begin
      while (pos <= length(s)) and not isFirstChar(s[pos]) do
         pos := pos + 1;
      if pos <= length(s) then begin
         w := w + s[pos]; 
         pos := pos + 1;
         while (pos <= length(s)) and isWordChar(s[pos]) do begin
            w := w + s[pos];
            pos := pos + 1;
         end;
         i := length(w);
         while (i > 0) and not isLastChar(w[i]) do begin
            Delete(w, i, 1);
            i := i - 1;
            pos := pos - 1;
         end;   
      end;   
   end;      
end; 

function char2caps(ch: char): char;
begin
   if ch = 'ё' then
      char2caps := 'Ё'
   else if (ch >= 'а') and (ch <= 'я') then
      char2caps := chr(ord(ch) - (ord('а') - ord('А')))
   else if (ch >= 'a') and (ch <= 'z') then
      char2caps := chr(ord(ch) - (ord('a') - ord('A')))
   else
      char2caps := ch
end;

procedure Str2Caps(var s: string);
var
   i: integer;
begin
   for i := 1 to length(s) do
      s[i] := char2caps(s[i]);
end;

begin
   Assign(f, 'case_text.txt');
   Assign(output, 'res2.txt');
   Reset(f);
   while not eof(f) do begin
      Readln(f, s);
      count := count + 1;
      ArrayAppendString(Sentences, s);
      pos := 1;
      GetWord(s, pos, w);
      while w <> '' do begin
         Str2Caps(w);
         Add2Table(Table, w);
         GetWord(s, pos, w);
      end;
   end;
   Close(f);
   SetLength(a, count, count);
   for pos := 0 to Length(Table) - 1 do
      foreach i in Table[pos].data do
         foreach j in Table[pos].data do
            a[i - 1, j - 1] := a[i - 1, j - 1] + 1;
   for i := 0 to count - 1 do
      for j := i + 1 to count - 1 do
         if a[i, j] > n then begin
            Writeln(i + 1, ', ', j + 1, ') ', a[i, j], ' совпадающих слов');
            Writeln(Sentences[i]);
            Writeln(Sentences[j]);
            Writeln;
         end
end.