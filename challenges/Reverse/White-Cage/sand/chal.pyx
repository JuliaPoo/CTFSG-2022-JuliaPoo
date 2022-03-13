import re

N = 0
def fff(a):
  global N; N+=1
  return a

verify = (
    
lambda h,e,w,r,o:h(e(h(h(w)(e(1)))(e(0))))(h(e(h(o(lambda f:lambda a:lambda b:(lambda c:lambda d:lambda i:lambda g:c(a)(c(b)(e)(e(w)))(g(d(a))(d(b))(lambda 

                                                   x
                                                   :f(i(a))(
                                                  i(b))(x))(e(w
                                                  ))))(h(w)(e(e)))
                                                      (h(e(h(w)(e(e))
                                                       ))(h(w)(e(e(w))))
                                                         )(h(e(h(w)(e(e(w))
                                                   )))(h    (w)(e(e(w)))))(h(e
                                                           (h(h(e(h(e(h(h(h)(e(h(
                                                    e(h      (h)(e(e))))(h(e(e))(h(e
                                                        (h))(h(e(h(w)))(e)))))))(e(h(e
                                                     (h(e     (h(e(h(h)(e(e))))(h(e(e))(h
                                                        (h)   (e(e(w)))))))))(h(e(h(h)(e(h(
                                                            e(h(e(h(e(h(w)))(e)))))(h(e(h(w))
                                                          )(e))))))(e))))))(e))))(e(e(w)))))(h
                                                               (e(h(h(e(h))(h(e(h(h)(e(h(e(h(h)
                                                             (e(h(e(e))(h(e(h))(e))))))(h(e(e))(
                                                               h(e(h(h)))(e)))))))(h(e(h(e(h))))(
                                                             h(e(h(h)(e(h(e(h(h)(e(h(e(e))(h(e(h))(             e))))))(h(e(e)
                                                                )(h(e(h(h)))(h(e(e))(h(e(h(h)(e(e))))   (h(e(e))(h))))))))))(h
                                                               (e(e))(h(e(h))(h(e(e))(h(e(h(e(h(e(h(h)(e(h(h(h))(e)(h)))))(
                                                                 e)))))(h(e(h(h)(e(e))))(h(e(e))(h(e(h))(h(e(h))(h(e(e))(
                                                                  h(e(h(e(w))))(h(e(h))(h(e(e))(h(e(h(h)))(h(e(e))(e))
                                                                  )))))))))))))))))))(h(e(h(e(e))))(h(e(h(h)(e(h(e(h
                                                                  (w)))(h(e(e))(e))))))(h(e(e))(h(e(h(h)))(h(e(e)
                                                                  )(e)))))))(e))))(e(h(e(h(h(h)(e(e(h(h(e(h(h(
                                                                 w)(e(h(h(e(h))(e)))))))(e))(h(h(e(h))(e)))
                                                              (h(e(h(h(h(e(h))(e)))))(e)(h(h(e(h(h(w)(e(
                                                           h(h(e(h))(e)))))))(e))(h(h(e(h))(e)))(h(h
                                                      (e(h))(e))(h(h(e(h))(e))(w))))(w))))))(e(h
                                               (e(h(h(w)(e(h(h(e(h))(e)))))))(e)(h(e(h(h(
                                          h(e(h))(e)))))(e)(h(
                                         h(e(h))(e))(w))
                                          (h(h(e(h))
                                              (e




                                                                                   ))(    w
                                                                            )    ))(h(  e(h(
                                                                           h(h   (e(h   ))(   e
                                                                         )))))(  e)(h  (h(e  (h)
                                                                     )(e))(h(h(e(h))(e))(h(h(e(
                                                                    h))(e))(w))))(h(h(e(h))(e))
                                                                (w)))))))(h(e(h(h)(e(h(e(h(h)(
                                                              e(h(e(h(e(h(e(h))(h(e(e))(h(e(h
                                                           ))(h(e(e))(h(e(h(w)))))))))))(h(
                                                        e(h(h)(e(h(e(e))(h(e(h(h)))(h(e(e)
                                                      )(e)))))))(h(e(e))(h(e(h(h)))(h(e(e
                                                     ))(h(e(h(e(h(w)))))(h(h(e(h))(h(e(e
                                                   ))(h(e(h(h)))(h(e(e))(e)))))(h(e(h(
                                                 e(h(e(h(w)))(h(e(h(h)(e(e(h(h(e(h(h(w
                                                )(e(h(h(e(h))(e)))))))(e))(h(h(e(h))(e
      )))(h                                    (h(e(h))(e))(h(e(h(h(h(e(h))(e)))))(
     e)(h(h(e(h))                             (e))(h(h(e(h))(e))(h(h(e(h))(e))(h
     (h(e(h))(e))(h(                         h(e(h))(e))(w))))))(w))))))))(h(e
       (h(w)))(h(e(h(h)(                    e(e(h(h(e(h))(e))(h(h(e(h(h(w)(e(
          h(h(e(h))(e)))))))(e)             )(h(h(e(h))(e)))(h(h(e(h))(e))(h(
             h(e(h))(e))(h(h(e(h))(e))(h(e(h(h(h(e(h))(e)))))(e)(h(h(e(h))(e))(h(h(e(h)
                )(e))(w)))(h(h(e(h))(e))(w))))))))))))(h(w)))))))))(h(e(h(h)(e(h(e(h(w)))(h
                    (e(h(h)(e(e(h(e(h(h(w)(e(h(h(e(h))(e)))))))(e)(h(h(e(h(h(h(e(h))(e))
                           )))(e))(h(h(e(h))(e)))(h(h(e(h))(e))(w)))(h(e(h(h(h(e(h))(
                                    e)))))(e)(h(h(e(h))(e))(w))(h(h(e(h))(e))(h(h(e
                                   (h))(e))(h(h(e(h))(e))(w))))))))))(h(e(h(w)
                                ))(h(e(h(h)(e(e(h(h(e(h))(e))(h(e(h(h(h(e
                             (h))(e)))))(e)(h(h(e(h))(e))(h(h(e(h))
                         (e))(h(h(e(h))(e))(h(h(e(h))(e))(h(h
                     (e(h))(
                e))(w))
           ))))(w)
      ))))))(






                                                        h(
                                                   w))))))
                                                )))(h(e(e)
                                              )(h(e(h(h)
                                           ))(h(e(e))(e
                                         ))))))))))))
                                      ))))(h(e(e))(h
                                    (e(h(h)))(h(e(e
                                  ))(h(e(h(e(h(e(h(h(e
                                (h))(h(e(e))(h(e(h   (h)
                              ))(h(e(e))(e)))))))(
                             h(e(h(h)(e(h(e(h(h)(e(h
                            (w)))))(h(e(e))(h(e(h(h))
                           )(h(e(e))(e))))))))(h(e(
                          e))(h(e(h))(e))))))))(h(
      e(h(h)(e(h(        e(h(h)(e(h(w)))))(h(e(e))(
       h(e(h(h)))(h(e(e))(e))))))))(h(e(e))(h(e(h
         ))(h(e(e))(h(e(h(e(h(w)))))(h(e(h(h)(e(h
           (w)))))(h(e(e))(h(e(h(h)))(h(e(e))(e)
             )))))))))))))))))(h(e(h(e(h(e(h))(
                h(e(e))(h(e(h(h)(e(e(h(h(e(h))(e                            )  )(
                  h(h(e(h))(e))(h(h(e(h(h(w)(e(h                            (h  (e (h
                    ))(e)))))))(e))(h(h(e(h))(e))                         )(h(h (e (h(
                       h(w)(e(h(h(e(h))(e)))))))(e))                       (h(h(e(h))(e))
                           )(h(e(h(h(h(e(h))(e)))))(e)(h                   (h(e(h))(e))(h(h
                                (e(h))(e))(w)))(h(h(e(h))(e)                )(w)))))))))))(h(
                                                    e(h))(h(e(e))             (h(e(h(e(h(h(e(h(
                                                       e(h(h(e(h(              e(h(h(h)(e(e(h(e(h
                                                          (e(h(                e(h(h)(e(e))))(h(e(
                                                                                e))(h(e(h))(h(e(h(w
                                                                                  )))(e))))(e(w)))))                )(h(e
                                                                                   (h(h)(e(h(e(e))(h(            e(h))(h(
                                                                                    e(h(w)))(e)))))))       (h(e(e))(h(
                                                                             e(h(h(h)(e(e)))))(e))))))))(e(h(e(h(h(h(
                                                                              e(h))(e)))))(e)(h(h(e(h))(e))(h(h(e(
                                                                                h))(e))(h(e(h(h(h(e(h))(e)
                                                                                   ))))(e)(h(h(e(h))(e))(h
                                                                                        (h(e(h))(e))(w)))(w))
                                                                                             ))(w)))))(h(e(h(h)
                                                                                                                (e(
                                                                                                                   e)))









                                                                                )  (h(e(h(e(h))(h(
                                                                                    w)))))))))(e(h(h(
                                                                                  e(h(h)(e(e(e(w))))))(
                                                                                    h(e(h(w)))(h(e(e))(h
                                                                                    (e(h(h)(e(e))))(h(e(e)        )(h(e(h(
                                                                                     h(h(w)(e(h(h(e(h))(e))))))))(e))))))
                                                                                      )(h(h(e(h))(e)))(h(h(e(h))(e))(h
                                                                                      (e(h(h(h(e(h))(e)))))(e)(h(h(
                                                                                      e(h))(e))(h(h(e(h))(e))(w
                                                    )                             ))(w)))))))(h(h(e(h))(h(e
                                               (e  ))  (h                  (e(h(h)))(h(e(e))(e))))))
                                            )))(e(h(h(e(h(h(           w)(e(h(h(
                                         e(h))(e)))))))(e))
                                      (h(h(e(h))(e)))(h(e
                                   (h(h(h(e(h))(e)))))(e
                                 )(h(h(e(h))(e))(h(h(e
                               (h))(e))(h(h(e(h))(e))(
     h(h(e(h                  ))(e))(h(h(e(h))(e))
      (w))))))(w             ))))))))(h(e(h(h)(e(
          h(e(h(e(h(e(h))(h (e(e))(h(e(h))(h(e(e))(h(e
              (h(e(h(w)))(h(e(h(h)(e(e(h(h(e(h(h(w)(e(h
                        (h(e(h))(e)))))))(e))(h(h(e(
                      h))(e)))(h(h(e(h))(e))(h
                 (h(e(h))(e))(w))))))))
            (h(e
        (h









            (w)))
           (h(e(h(
           h)(e(e(h  (
           h(e(h(h(w)(e
          (h(h(e(h))(e))
          )))))(e))(h(h(e(
          h))(e)))(h(h(e(h)
          )(e))(h(e(h(h(h(e(
        h))(e)))))(e)(h(h(e(h
 ))(e))(h(h(e(h))(e))(w)))(w)))
   )))))(h(e(h(w)))(h(e(h(h)(e(e(h(e(h(h(w
      )(e(h(h(e(h))(e)))))))(e)(h(e(h(h(h
           (e(h))(e)))))(e)(h(h

                                              (e(h))(e))(w
                                               ))(h(h(e(h))(e))
                                                 (h(h(e(h))(e))(h(h
                                                   (e(h))(e))(w)))))(h
                                                   (e(h(h(h(e(h))(e)))))(
                                                  e)(h(h(e(h))(e))(h(h(e(h)
                                                 )(e))(h(h(e(h))(e))(w))))(h(
                                                h(e(h))(e))(w))))))))(h(e(h(w))
                                                )(h(e(h(h)(e(e(h(e   (h(h(h(e(h))(e
                                               )))))(e)(h(h(e(h)            )(e))
                                               (h(h(e(h))(e))
                                               (h(h(e(h)  )
                                              (e))(h(h  (
                                              e(h))(e )                                                           )(w)
                                              ))))  (                                                          w)))))
                                              )(h(e(                                                        h(w)))(
                                              h(e(h(                                                     h)(e(e(h(h
                                             (e(h))                                                    (e))(h(h(e( h)
                                              )(e                                                    ))(h(h(e(h))(e
                                                                                                    ))(h(h(e(h))(e
                                                                                        ))(h(      h(e(h(h(h(e(h))
                                                                                         (e)))))(e))(h(h(e(h))(e)
                                                                                           ))(h(h(e(h))(e))(w)))
                                                                                              ))))))))(h(w))))))
                                                                                                 )))))))))))))))(h
                                                                                                     (h(e(h))(h(e(e))(
                                                                                                                   h(e(h(h
                                                                                                                       )




                                                                                                           ))(h(e(e)
                                                                                                     )(e))))))))))(
                                                                                                 h(e(e))(h(e(h(h)
                                                                                             ))(e)))))))))))))(
                                                                                           h(h(e(h))(h(e(e))(h(
                                                                                         e(h))(h(e(e))(h(e(h))(h
                                                                                       (e(e))(h(e(h(e(h(e(h(h)(e(
                                                                                                 e))))(h(e(e))(h(e
                                                                                                 (h))(h(e(h(w)))(h
                                                       (e(h(h                                      )(e(e(h(h(e(h))(
                                                         e))(h(e(                                     h(h(h(e(h))(e
                                                           )))))(e)(h                                     (h(e(h))(
                                                            e))(h(h(e(h)                                 )  (e))(h(
                                                           h(e(h))(e))(h(h                                 ( e(h))(e
                                                            ))(w)))))(h(h(e(                                 h ))(e)
                                                             )(w))))))))(h(w))))))))))(h                      ( h(e(
                                                              h))(h(e(e))(h(e(h(h)))(                         h(e(e)
                                                              )(e)))))(h(e(h(e(h(w                             )))))
                                                           (h(h(e(h))(h(e(e))(                                   h(e
                                 (h (h ))           )(h(e(e))(e)))))(h
                              (e(h(e(h(e(h         (w)))
                           (h(e(h(h)(e(e(
                        h(h(e(h))(e))(h
                      (h(e(h(h(w)(e(h(
  h(e(h             ))(e)))))))(e))
   (h(h(e(h))      (e)))(h(e(h(h(h
        (e(h))(e)))))(e)(h(h(e(h))(e))(
               h(h(e(h))(e))(h(h(e(h
             ))(e))(h(h(e(h))(








       e))(
      h(h(e(
      h))(e))(w
     ))))))(w)))
     )))))(h(w))))
      )))(h(e(h(h)(
 e(h(e(h(w)))(h(e(h(
h)(e(e(h(h(e(h(h(w)(e(h(h(e(h
   ))(e)))))))(e))(h(h(e(h))
         (e)))(h(h(                           e(h))(e)
                                                )(h(h(e(h))
                                                 (e))(h(e(h(h(
                                                h(e(h))(e)))))(e
                                               )(h(h(e(h))(e))(h(h
                                               (e(h))(e))(w  )))(w))))
                                               )))))(h(w)                                       )
                                              )))))(                                        h(e(e
                                              ))(h                                        (e(h(
                                              h))                                      )(h(e(e)
                                              )(e)                                   ))))))))))
                                              )))                                   ))(h(e(h(e
                                              (                              h(h(e(h))(h(e(e)
                                                                               )(h(e(h(h)))(h
                                                                                  (e(e))(e))))
                                                                                      )))))(h(e(h(
                                                                                                 h)(






                                                                                                                            e
                                                                                                                        (h(e(e))(
                                                                                                                    h(e(h))(h(e(
                                                                                                                  e))(h(e(h(e(
                                                                                                  h             (e(h(w)))(h(e
                                                                                                  (h(h)(       e(e(h(e(h(h(
                                                                                                      h(e(h))(e)))))(e)(h(h(e(
                                                                                                           h))(e))(w))(h(h









                                             (
                                            e    (h))
                                            (  e)    )
                                             (h(h(                                                         e(h))(e))(h(h(e(h
                                            ))(e))(                                                   w)))))))))(h(w))))))
                                           )(h(e(h(h                                                  )(e(h(    w)))))(h(e
                                      (e))(h(e(h (h)))(h(e                                            (e          ))(e))
                                  ))))) ) )) ) )  ( h(e  (e))                                                      (h(e
                         (h(h   )  )   )     ( h  (  e (   e))(h                                                  (e(
                       h(e(h(e(  h          (  h  )   (  e   (  e)
                      )))(h(e   (   e   )   )  (   h      (    e  (
                      h))(h(w )    )   )   )   )   )   )   )    (   h                (e(h
                      (h)(e(e)             )   )   )    (   h    (   e                 (e))(
                        h(e(h))       (    h   (        e         (   h                (w)))(h
                       (   e     (    h    (   h    (    w         )   (               h(h(w)(h(
                      h    (    w    )         (  e(h(e( h    (         h               )(e(e))))
                     (    h          (         e(e))(h(e (          h    )              )(h(e(h(w)))(e)))
                    )    (     e     )    (    e))))(e(h  (    h     (    e              (h(h(w)(e(h(h(
                    e    (     h    )     )   (e)))))))(  e          )    )              (h(h(e(h(h(w
                   )                (     e (h(h(e(h))(e) )           )    )         )))(e))(h(h(
                   e    (     h     )     )(e))))(h(e(h(h (     h     (    e      (h))
                  (     e     )     )     )))(e)(h(h(e(h  )           )     (
                  e                 )    )(h(h(e(h))(e))                    (
                  h    (            h   (e(h))(e))(h(h     (           e    (
                  h    )            )   (e))( w))))  )     (           w    )
                  )    )           ))  )(e(h  (e(   h(h    (           h    (
                  e(h))(e))  ))    )( e)(h(  h(e(   h)    )(    e)  )(h(e(h(h
                  (    h      (     e(h)  )    (     e     )           )    )
                  )    )           (e)    (    h           (           h    (
                  e    (           h)     )    (           e                )
                  )    (            h     (    h           (                e
                  (    h            )     )    (                            e
                  )    )            (     w    )                            )
                  )    (            w     )    )                            )
                  (    w            )     )    )                            )
                  )    )            )     (    e                            )
                  )    )            )     )    )                            )
                  )    )            )     )    )          )                 )
                  )    (            h     (    h          (                 e
                  (    h            )     )    (          e                 )
                  )    (      h    (h     (    e    (h    ))          (e    )
                  )    (h    (e    (h    (h    (h   (e    (h    ))    (e    )
                 ))))(e)(h(h(e(h))(e))(h(h(e(h))(e))(w)))(w))))))))(o(lambda y:
                lambda z:h(e(h(e(h(e(h(h)(e(e))))(h(e(e))(h(e(h))(h(e(h(w)))(e))
                
))(e(w))))))(h(e(h(h)(e(h(e(e))(h(e(h))(h(e(h(w)))(e)))))))(h(e(e))(h(e(h(h(h)(e(e)))))(e))))(lambda x:y(z[1:])(x))(o(lambda y:
lambda m: h(h(e(h))(e))(y(r(m))) if r(m) else w)(z[0])) if z else  h(e(h(h)(e(e))))(h(e(e))(h(e(h))(h(e(h(w)))(e))))(e)(e)))))(
lambda x:lambda y:lambda z:x(z)(y(z)),lambda x:lambda y:x,lambda x:x,lambda n:fff(n+2022)%127,lambda f:(lambda g:f(g(g)))(lambda g
:f(lambda y: g(g)(y))))

import time

t = time.time()

ALLOWED = b"_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM{}"

def SideChannel(b:list)->int:

    global N; N = 0
    verify(b)
    return N

flag = []
while True:

    for c in ALLOWED:
        d = abs(SideChannel(flag+[c,0]) - SideChannel(flag+[c,1]))
        if d != 0:
          break

    flag += [c]
    flagpt = bytes(flag).decode('utf-8')
    print(f"{flagpt}" + " "*15)

    if verify(flag):
        break

print(f"DONE {time.time()-t}s")