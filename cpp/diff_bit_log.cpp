#include <bits/stdc++.h>

using namespace std;

int main(int argc, const char *argv[])
{

    if (argc != 4)
    {
        printf("usage: <src-filename> <dst-filename> <log-filename>\n");
        return -1;
    }

    FILE *f1 = fopen(argv[1], "rb");
//    FILE *f1 = fopen("/home/liudeyuan/Desktop/retention/data/data1/writers.0.0", "rb");
    if (!f1)
    {
        printf("Fail to open file <%s>\n", argv[1]);
        return -1;
    }

    FILE *f2 = fopen(argv[2], "rb");
//    FILE *f2 = fopen("/home/liudeyuan/Desktop/retention/data/data1/writers.0.1", "rb");
    if (!f2)
    {
        printf("Fail to open file <%s>\n", argv[2]);
        fclose(f1);
        return -1;
    }

    FILE *log = fopen(argv[3], "w");
//    FILE *log = fopen("/home/liudeyuan/Desktop/log", "w");
    if (!log)
    {
        printf("Fail to open file <%s>\n", argv[3]);
        fclose(f1);
        fclose(f2);
        return -1;
    }

    unsigned char buf1[1024 * 1024];
    unsigned char buf2[1024 * 1024];
    unsigned char masks[8] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80};
    unsigned long long offset = 0;
    while (!feof(f1) && !feof(f2))
    {
        int ret1 = fread(buf1, 1024 * 1024, 1, f1);
        int ret2 = fread(buf2, 1024 * 1024, 1, f2);
        if (!ret1 || !ret2)
        {
            break;
        }

        for(int i = 0; i < 1024 * 1024; i++)
        {
            for(int j = 0; j < 8; j++)
            {
                if((buf1[i] & masks[j]) ^ (buf2[i] & masks[j]))
                {
                    string s = to_string(offset+j) + "\n";
                    printf("%s", s.c_str());
                    fwrite(s.c_str(), s.size(), 1, log);
                }
            }
            offset += 8;
        }

    }

    fclose(f1);
    fclose(f2);
    fclose(log);

    return 0;
}
