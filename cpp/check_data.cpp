#include <bits/stdc++.h>

using namespace std;

int main(int argc, const char *argv[])
{

    if (argc != 3)
    {
        printf("usage: <src-filename> <log-filename>\n");
        return -1;
    }

    FILE *f = fopen(argv[1], "rb");
    if (!f)
    {
        printf("Fail to open file <%s>\n", argv[1]);
        return -1;
    }

    FILE *log = fopen(argv[2], "a");
    if (!log)
    {
        printf("Fail to open file <%s>\n", argv[2]);
        fclose(f);
        return -1;
    }

    unsigned char buf[1024 * 1024];
    unsigned char masks[8] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80};
    unsigned long long offset = 0, cnt = 0;
    while (!feof(f))
    {
        int ret = fread(buf, 1024 * 1024, 1, f);
        if (!ret)
        {
            break;
        }

        for(int i = 0; i < 1024 * 1024; i++)
        {
            for(int j = 0; j < 8; j++)
            {
                if(buf[i] & masks[j])
                {
                    ++cnt;
                }
            }
            offset += 8;
        }
    }

    string s = to_string(cnt) + " " + to_string(offset) + " " + to_string(100 * cnt / offset) + "%\n";
    fwrite(s.c_str(), s.size(), 1, log);

    fclose(f);
    fclose(log);

    return 0;
}
