#include <stdlib.h>
#include <stdio.h>
#include "extmem.h"

void sort(unsigned char *blk[8], int numOfMember);
void join();

int main(int argc, char **argv)
{
    Buffer buf; /* A buffer */
    unsigned char *blk[8] = {NULL}; /*pointers to a block */
    int numOfMember = 4;
    int addr = 1;
    int writeAddr = 101;
    int i, j, k;
    char str[5];
    int blkCount[5] = {0};

    /* Initialize the buffer */
    if(!initBuffer(520, 64, &buf))
    {
        perror("Buffer Initialization Failed!\n");
        return -1;
    }

    printf("对关系R的子表按R.A从大到小顺序进行排序：\n");
    printf("将进行组内排序后的数据写入到");
    for(i = 0; i < 4; i++)
    {
        for(j = 0; j < numOfMember; j++)
        {
            blk[j] = readBlockFromDisk(addr, &buf);
            addr++;
        }
        sort(blk, numOfMember);
        for(j = 0; j < numOfMember; j++)
        {
            itoa(writeAddr + 1, str, 10);
            for(k = 0; k < 4; k++)
            {
                *(blk[j] + 8 * 7 + k) = str[k];
            }
            if(writeBlockToDisk(blk[j], writeAddr, &buf) == 0)
            {
                printf("%d ", writeAddr);
                writeAddr++;
            }
            freeBlockInBuffer(blk[j], &buf);
        }
    }
    printf("磁盘块中\n");
    freeBuffer(&buf);

    numOfMember = 8;
    addr = 17;
    writeAddr = 117;
    for(i = 0; i < 5; i++)
    {
        blkCount[i] = 0;
    }

    /* Initialize the buffer */
    if(!initBuffer(520, 64, &buf))
    {
        perror("Buffer Initialization Failed!\n");
        return -1;
    }

    printf("\n对关系S的子表按S.C从大到小顺序进行排序：\n");
    printf("将进行组内排序后的数据写入到");
    for(i = 0; i < 4; i++)
    {
        for(j = 0; j < numOfMember; j++)
        {
            blk[j] = readBlockFromDisk(addr, &buf);
            addr++;
        }
        sort(blk, numOfMember);
        for(j = 0; j < numOfMember; j++)
        {
            itoa(writeAddr + 1, str, 10);
            for(k = 0; k < 4; k++)
            {
                *(blk[j] + 8 * 7 + k) = str[k];
            }
            if(writeBlockToDisk(blk[j], writeAddr, &buf) == 0)
            {
                printf("%d ", writeAddr);
                writeAddr++;
            }
            freeBlockInBuffer(blk[j], &buf);
        }
    }
    printf("磁盘块中\n");
    freeBuffer(&buf);

    join();
    return 0;
}

void sort(unsigned char *blk[8], int numOfMember)
{
    int i, j, k, m, n;
    int X, Y;
    int maxPosi, maxPosj, unchanged;
    char str[5];
    char temp;

    for(i = 0; i < numOfMember; i++)
    {
        for(j = 0; j < 7; j++)
        {
            for(k = 0; k < 4; k++)
            {
                str[k] = *(blk[i] + j*8 + k);
            }
            X = atoi(str);
            unchanged = 1;

            n = j + 1;
            for(m = i; m < numOfMember; m++)
            {
                while(n < 7)
                {
                    for(k = 0; k < 4; k++)
                    {
                        str[k] = *(blk[m] + n*8 + k);
                    }
                    Y = atoi(str);
                    if(Y > X)
                    {
                        maxPosi = m;
                        maxPosj = n;
                        X = Y;
                        unchanged = 0;
                        // printf("%d, %d ", m, n);
                    }
                    n++;
                }
                n = 0;
            }
            // printf("\n%d, %d\n", maxPosi, maxPosj);
            if(unchanged == 0)
            {
                for(k = 0; k < 8; k++)
                {
                    temp = *(blk[i] + j*8 + k);
                    *(blk[i] + j*8 + k) = *(blk[maxPosi] + maxPosj*8 + k);
                    *(blk[maxPosi] + maxPosj*8 + k) = temp;
                }
            }
            // printf("%d ", X);
        }
        // printf("\n");
    }
/*  查看排序结果
    for(i = 0; i < numOfMember; i++)
    {
        for(j = 0; j < 7; j++)
        {
            for(k = 0; k < 4; k++)
            {
                str[k] = *(blk[i] + j*8 + k);
            }
            X = atoi(str);
            printf("%d ", X);
        }
    }
    printf("\n");
*/
    return;
}

void join()
{
    Buffer buf; /* A buffer */
    unsigned char *blk[8] = {NULL}; /*pointers to a block */
    int readRAddr = 101;
    int readSAddr[4] = {117, 125, 133, 141};
    int writeAddr = 201;
    int i, j, k;
    int A, C;
    char str[5];
    int blkCount[6] = {0};
    int notFinish = 1;
    int joinCount = 0;

    /* Initialize the buffer */
    if(!initBuffer(520, 64, &buf))
    {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    blk[5] = getNewBlockInBuffer(&buf);
    while(readRAddr < 117)
    {
        blk[4] = readBlockFromDisk(readRAddr, &buf);
        readRAddr++;
        blkCount[4] = 0;

        while(blkCount[4] < 7)
        {
            for(k = 0; k < 4; k++)
            {
                str[k] = *(blk[4] + blkCount[4] * 8 + k);
                blkCount[k] = 0;
            }
            A = atoi(str);
            blkCount[4]++;

            for(i = 0; i < 4; i++)
            {
                readSAddr[i] = 117 + i * 8;
                blk[i] = readBlockFromDisk(readSAddr[i], &buf);
                readSAddr[i]++;
            }

            while(1)
            {
                // S是否已经完全遍历
                notFinish = 0;
                for(i = 0; i < 4; i++)
                {
                    if(blkCount[i] < 7)
                    {
                        notFinish = 1;
                    }
                }
                if(!notFinish)
                {
                    break;
                }

                for(i = 0; i < 4; i++)
                {
                    if(blkCount[i] > 6)
                    {
                        continue;
                    }
                    else
                    {
                        for(k = 0; k < 4; k++)
                        {
                            str[k] = *(blk[i] + blkCount[i] * 8 + k);
                        }
                        C = atoi(str);
                        // printf("%d %d %d\n", C, readSAddr[i], blkCount[i]);
                        if(A == C)
                        {
                            joinCount++;
                            for(k = 0; k < 8; k++)
                            {
                                *(blk[5] + blkCount[5]*8 + k) = *(blk[4] + blkCount[4] * 8 + k);
                                *(blk[5] + blkCount[5]*8 + k + 8) = *(blk[i] + blkCount[i] * 8 + k + 8);
                            }

                            blkCount[5] += 2;
                            if(blkCount[5] == 8)
                            {
                                // 存入缓冲区
                                blkCount[5] = 7;
                                itoa(writeAddr + 1, str, 10);
                                for(k = 0; k < 4; k++)
                                {
                                    *(blk[5] + 8 * 7 + k) = str[k];
                                }
                                if(writeBlockToDisk(blk[5], writeAddr, &buf) == 0)
                                {
                                    printf("结果写入磁盘%d\n", writeAddr);
                                    writeAddr++;
                                    blk[5] = getNewBlockInBuffer(&buf);
                                }
                                blkCount[5] = 0;
                            }
                        }
                        else if(A > C)
                        {
                            blkCount[i] = 7;
                        }

                        // 后移一位
                        if((blkCount[i] == 6) && (readSAddr[i] % 8 != 5))
                        {
                            freeBlockInBuffer(blk[i], &buf);
                            blk[i] = readBlockFromDisk(readSAddr[i], &buf);
                            readSAddr[i]++;
                            blkCount[i] = 0;
                        }
                        else if(blkCount[i] != 7)
                        {
                            blkCount[i]++;
                        }
                    }
                }
            }
            for(k = 0; k < 4; k++)
            {
                freeBlockInBuffer(blk[k], &buf);
            }
        }
        freeBlockInBuffer(blk[4], &buf);
    }
    printf("\n总共连接%d次", joinCount);
    return;
}
